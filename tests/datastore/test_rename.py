import pytest
from api                import One
from utils              import get_unic_name
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test






@pytest.fixture
def datastore():
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
def datastore_2():
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



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    rename_if_not_exist__test(one.datastore)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_datastore(one: One, datastore: Datastore):
    rename__test(one.datastore, datastore)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_name_collision(one: One, datastore: Datastore, datastore_2: Datastore):
    cant_be_renamed__test(one.datastore, datastore, datastore_2.info().NAME)
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_datastore_name(one: One, datastore: Datastore):
    cant_be_renamed__test(one.datastore, datastore, "")



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_datastore_name(one: One, datastore: Datastore, bad_symbol: str):
    cant_be_renamed__test(one.datastore, datastore, f"{bad_symbol}")
    cant_be_renamed__test(one.datastore, datastore, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.datastore, datastore, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.datastore, datastore, f"Greg{bad_symbol}Vetkin")
