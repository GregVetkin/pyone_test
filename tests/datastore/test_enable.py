import pytest
import pyone
import random
from api            import One
from utils.other    import get_unic_name



@pytest.fixture
def system_datastore(one: One):
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = one.datastore.allocate(datastore_template, -1)
    yield datastore_id
    one.datastore.delete(datastore_id)


@pytest.fixture
def image_datastore(one: One):
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(datastore_template, -1)
    yield datastore_id
    one.datastore.delete(datastore_id)


@pytest.fixture
def file_datastore(one: One):
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(datastore_template, -1)
    yield datastore_id
    one.datastore.delete(datastore_id)






def test_datastore_not_exist(one: One):
    datastore_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        one.datastore.enable(datastore_id, True)



def test_not_for_file_datastore(one: One, file_datastore):
    datastore_id = file_datastore

    with pytest.raises(pyone.OneInternalException):
        one.datastore.enable(datastore_id, True)
    assert one.datastore.info(datastore_id, False).STATE == 0

    with pytest.raises(pyone.OneInternalException):
        one.datastore.enable(datastore_id, False)
    assert one.datastore.info(datastore_id, False).STATE == 0



def test_not_for_image_datastore(one: One, image_datastore):
    datastore_id = image_datastore

    with pytest.raises(pyone.OneInternalException):
        one.datastore.enable(datastore_id, True)
    assert one.datastore.info(datastore_id, False).STATE == 0

    with pytest.raises(pyone.OneInternalException):
        one.datastore.enable(datastore_id, False)
    assert one.datastore.info(datastore_id, False).STATE == 0



def test_enable_disable_system_datastore(one: One, system_datastore):
    datastore_id = system_datastore

    # Выключение
    _id = one.datastore.enable(datastore_id, False)
    assert _id == datastore_id
    assert one.datastore.info(datastore_id, False).STATE == 1

    # Включение
    _id = one.datastore.enable(datastore_id, True)
    assert _id == datastore_id
    assert one.datastore.info(datastore_id, False).STATE == 0
