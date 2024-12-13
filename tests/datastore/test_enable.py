import pytest
from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME




@pytest.fixture
def system_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def file_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneException):
        one.datastore.enable(999999, True)
    
    with pytest.raises(OneException):
        one.datastore.enable(999999, False)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_disable_file_datastore(one: One, file_datastore: Datastore):
    with pytest.raises(OneException):
        one.datastore.enable(file_datastore._id, True)
    assert file_datastore.info().STATE == 0

    with pytest.raises(OneException):
        one.datastore.enable(file_datastore._id, False)
    assert file_datastore.info().STATE == 0



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_disable_image_datastore(one: One, image_datastore: Datastore):
    with pytest.raises(OneException):
        one.datastore.enable(image_datastore._id, True)
    assert image_datastore.info().STATE == 0

    with pytest.raises(OneException):
        one.datastore.enable(image_datastore._id, False)
    assert image_datastore.info().STATE == 0



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_disable_system_datastore(one: One, system_datastore: Datastore):
    _id = one.datastore.enable(system_datastore._id, False)
    assert _id == system_datastore._id
    assert system_datastore.info().STATE == 1

    _id = one.datastore.enable(system_datastore._id, True)
    assert _id == system_datastore._id
    assert system_datastore.info().STATE == 0

