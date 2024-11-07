import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
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
        one.datastore.info(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_info(one: One, datastore: Datastore):
    api_datastore_info  = one.datastore.info(datastore._id)
    cli_datastore_info  = datastore.info()
    
    assert cli_datastore_info.ID    == api_datastore_info.ID
    assert cli_datastore_info.NAME  == api_datastore_info.NAME
    assert cli_datastore_info.UNAME == api_datastore_info.UNAME
    assert cli_datastore_info.UID   == api_datastore_info.UID
    assert cli_datastore_info.GNAME == api_datastore_info.GNAME
    assert cli_datastore_info.GID   == api_datastore_info.GID
    assert cli_datastore_info.TYPE  == api_datastore_info.TYPE
    assert cli_datastore_info.STATE == api_datastore_info.STATE
