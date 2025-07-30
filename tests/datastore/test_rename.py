import pytest
import pyone
from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test






@pytest.fixture
def taken_datastore_name(one: One):
    ds_name  = get_unic_name()
    template = f"""
        NAME    = {ds_name}
        DS_MAD  = dummy
        TM_MAD  = dummy
        TYPE    = IMAGE_DS
    """
    ds_id = one.datastore.allocate(template, -1)
    yield ds_name
    one.datastore.delete(ds_id)








def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


def test_rename(one: One, dummy_datastore):
    new_name = get_unic_name()
    rename__test(one.datastore, dummy_datastore, new_name)


def test_name_is_taken(one: One, dummy_datastore, taken_datastore_name):
    datastore_id = dummy_datastore
    new_name     = taken_datastore_name

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, new_name)
    


def test_empty_name(one: One, dummy_datastore):
    datastore_id = dummy_datastore
    new_name     = ""

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, new_name)





@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_datastore, char: str):
    datastore_id = dummy_datastore

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, f"{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, f"Gregory{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, f"{char}Vetkin")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.datastore, datastore_id, f"Gregory{char}Vetkin")

