import pytest

from api                            import One
from config.config                         import BAD_SYMBOLS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test





# =================================================================================================
# TESTS
# =================================================================================================




def test_host_not_exist(one: One):
    not_exist__test(one.host)



def test_rename_host(one: One, dummy_host):
    rename__test(one.host, dummy_host)



def test_host_name_collision(one: One, dummy_host):
    cant_be_renamed__test(one.host, dummy_host, "bufn1.brest.local")



def test_empty_host_name(one: One, dummy_host):
    cant_be_renamed__test(one.host, dummy_host, "")


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
def test_unavailable_symbols_in_host_name(one: One, dummy_host, bad_symbol: str):
    cant_be_renamed__test(one.host, dummy_host, f"{bad_symbol}")
    cant_be_renamed__test(one.host, dummy_host, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.host, dummy_host, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.host, dummy_host, f"Greg{bad_symbol}Vetkin")

