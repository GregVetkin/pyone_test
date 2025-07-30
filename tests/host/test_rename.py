import pytest
import pyone
from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test, not_exist__test







def test_host_not_exist(one: One):
    not_exist__test(one.host)



def test_rename(one: One, dummy_host):
    host_id = dummy_host
    new_name = get_unic_name()

    rename__test(one.host, host_id, new_name)



def test_name_is_taken(one: One, dummy_host):
    host_id = dummy_host
    new_name = one.hostpool.info().HOST[-1].NAME

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, new_name)




def test_empty_name(one: One, dummy_host):
    host_id = dummy_host
    new_name = ""

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_host, char: str):
    host_id = dummy_host

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, f"{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, f"Gregory{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, f"{char}Vetkin")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.host, host_id, f"Gregory{char}Vetkin")

