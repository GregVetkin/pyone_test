import pytest

from api                            import One
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test






def test_host_not_exist(one: One):
    not_exist__test(one.host)



def test_rename(one: One, dummy_host):
    rename__test(one.host, dummy_host)



def test_name_collision(one: One, dummy_host):
    existed_host_name = one.hostpool.info().HOST[-1].NAME
    cant_be_renamed__test(one.host, dummy_host, existed_host_name)



def test_empty_name(one: One, dummy_host):
    cant_be_renamed__test(one.host, dummy_host, "")


@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_host, char: str):
    cant_be_renamed__test(one.host, dummy_host, f"{char}")
    cant_be_renamed__test(one.host, dummy_host, f"Greg{char}")
    cant_be_renamed__test(one.host, dummy_host, f"{char}Vetkin")
    cant_be_renamed__test(one.host, dummy_host, f"Greg{char}Vetkin")

