import pytest
from api                            import One
from utils.other                    import get_unic_name
from config.config                         import BAD_SYMBOLS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test





@pytest.fixture
def taken_datastore_name(one: One):
    ds_name  = get_unic_name()
    template = f"""
        NAME    = {ds_name}
        DS_MAD  = dummy
        TM_MAD  = dummy
        TYPE    = IMAGE_DS
    """
    ds_id = one.datastore.allocate(template)
    yield ds_name
    one.datastore.delete(ds_id)



# =================================================================================================
# TESTS
# =================================================================================================




def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


def test_rename_datastore(one: One, dummy_datastore):
    rename__test(one.datastore, dummy_datastore)


def test_datastore_name_collision(one: One, dummy_datastore, taken_datastore_name):
    cant_be_renamed__test(one.datastore, dummy_datastore, taken_datastore_name)
    


def test_empty_datastore_name(one: One, dummy_datastore):
    cant_be_renamed__test(one.datastore, dummy_datastore, "")



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
def test_unavailable_symbols_in_datastore_name(one: One, dummy_datastore, bad_symbol: str):
    cant_be_renamed__test(one.datastore, dummy_datastore, f"{bad_symbol}")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"Gregory{bad_symbol}")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"Gregory{bad_symbol}Vetkin")
