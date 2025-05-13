import pytest
from api            import One
from pyone          import OneInternalException, OneNoExistsException
from utils.other    import get_unic_name



@pytest.fixture
def system_datastore(one: One):
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = one.datastore.allocate(datastore_template)
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
    datastore_id = one.datastore.allocate(datastore_template)
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
    datastore_id = one.datastore.allocate(datastore_template)
    yield datastore_id
    one.datastore.delete(datastore_id)



# =================================================================================================
# TESTS
# =================================================================================================


def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.enable(999999)



def test_cant_enable_disable_file_datastore(one: One, file_datastore):
    file_ds_id = file_datastore

    with pytest.raises(OneInternalException):
        one.datastore.disable(file_ds_id)
    assert one.datastore.info(file_ds_id).STATE == 0

    with pytest.raises(OneInternalException):
        one.datastore.enable(file_ds_id)
    assert one.datastore.info(file_ds_id).STATE == 0



def test_cant_enable_disable_image_datastore(one: One, image_datastore):
    image_ds_id = image_datastore

    with pytest.raises(OneInternalException):
        one.datastore.disable(image_ds_id)
    assert one.datastore.info(image_ds_id).STATE == 0

    with pytest.raises(OneInternalException):
        one.datastore.enable(image_ds_id)
    assert one.datastore.info(image_ds_id).STATE == 0



def test_enable_disable_system_datastore(one: One, system_datastore):
    system_ds_id = system_datastore

    result = one.datastore.disable(system_ds_id)
    assert result == system_ds_id
    assert one.datastore.info(system_ds_id).STATE == 1

    result = one.datastore.enable(system_ds_id)
    assert result == system_ds_id
    assert one.datastore.info(system_ds_id).STATE == 0
