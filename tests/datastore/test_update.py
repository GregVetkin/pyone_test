import pytest

from api                import One
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test



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
    update_if_not_exist__test(one.datastore)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_datastore__replace(one: One, datastore: Datastore):
    update_and_replace__test(one.datastore, datastore)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_datastore__merge(one: One, datastore: Datastore):
    update_and_merge__test(one.datastore, datastore)
