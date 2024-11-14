import pytest

from api                import One
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test


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
    


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    info_if_not_exist__test(one.datastore)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_info(one: One, datastore: Datastore):
    info__test(one.datastore, datastore)

