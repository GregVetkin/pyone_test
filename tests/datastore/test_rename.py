import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def datastore_2():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.rename(99999, "GregoryVetkin")



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_rename_datastore(one: One, datastore: Datastore):
    new_name = "api_test_new_ds_name"
    one.datastore.rename(datastore._id, new_name)
    assert datastore.info().NAME == new_name



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_name_collision(one: One, datastore: Datastore, datastore_2: Datastore):
    datastore_old_name = datastore.info().NAME
    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, datastore_2.info().NAME)
    datastore_new_name = datastore.info().NAME
    assert datastore_old_name == datastore_new_name



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_empty_datastore_name(one: One, datastore: Datastore):
    datastore_old_name = datastore.info().NAME
    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, "")
    datastore_new_name = datastore.info().NAME
    assert datastore_old_name == datastore_new_name



@pytest.mark.parametrize("symbol", ["$", "#", "&", "\"", "\'", ">", "<", "/", "\\", "|"])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unavailable_symbols_in_datastore_name(one: One, datastore: Datastore, symbol: str):
    datastore_old_name = datastore.info().NAME

    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, f"test{symbol}")

    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, f"{symbol}test")
    
    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, f"te{symbol}st")
    
    with pytest.raises(OneActionException):
        one.datastore.rename(datastore._id, f"{symbol}")

    assert datastore.info().NAME == datastore_old_name

