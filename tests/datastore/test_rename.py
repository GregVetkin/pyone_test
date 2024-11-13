import pytest
from api                import One
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import rename_unavailable_symbol__test
from tests._common_tests.rename import rename_empty_name__test
from tests._common_tests.rename import rename_collision__test


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
    rename_if_not_exist__test(one.datastore)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_rename_datastore(one: One, datastore: Datastore):
    rename__test(one.datastore, datastore)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_name_collision(one: One, datastore: Datastore, datastore_2: Datastore):
    rename_collision__test(one.datastore, datastore, datastore_2)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_empty_datastore_name(one: One, datastore: Datastore):
    rename_empty_name__test(one.datastore, datastore)


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unavailable_symbols_in_datastore_name(one: One, datastore: Datastore, bad_symbol: str):
    rename_unavailable_symbol__test(one.datastore, datastore, bad_symbol)


