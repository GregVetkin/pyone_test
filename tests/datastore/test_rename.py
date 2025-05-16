import pytest
from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
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








def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


def test_rename(one: One, dummy_datastore):
    rename__test(one.datastore, dummy_datastore)


def test_name_collision(one: One, dummy_datastore, taken_datastore_name):
    cant_be_renamed__test(one.datastore, dummy_datastore, taken_datastore_name)
    


def test_empty_name(one: One, dummy_datastore):
    cant_be_renamed__test(one.datastore, dummy_datastore, "")



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_datastore, char: str):
    cant_be_renamed__test(one.datastore, dummy_datastore, f"{char}")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"Gregory{char}")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"{char}Vetkin")
    cant_be_renamed__test(one.datastore, dummy_datastore, f"Gregory{char}Vetkin")
