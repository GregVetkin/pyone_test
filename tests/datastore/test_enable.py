import pytest
from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def system_datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image_datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def file_datastore():
    datastore_template = """
        NAME   = api_test_file_ds
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.enable(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_disable_file_datastore(one: One, file_datastore: Datastore):
    with pytest.raises(OneInternalException):
        one.datastore.disable(file_datastore._id)
    assert file_datastore.info().STATE == 0

    with pytest.raises(OneInternalException):
        one.datastore.enable(file_datastore._id)
    assert file_datastore.info().STATE == 0



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_disable_image_datastore(one: One, image_datastore: Datastore):
    with pytest.raises(OneInternalException):
        one.datastore.disable(image_datastore._id)
    assert image_datastore.info().STATE == 0

    with pytest.raises(OneInternalException):
        one.datastore.enable(image_datastore._id)
    assert image_datastore.info().STATE == 0



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_disable_system_datastore(one: One, system_datastore: Datastore):
    one.datastore.disable(system_datastore._id)
    assert system_datastore.info().STATE == 1

    one.datastore.enable(system_datastore._id)
    assert system_datastore.info().STATE == 0