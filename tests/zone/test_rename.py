import pytest
from api                import One
from utils              import get_unic_name
from one_cli.zone       import Zone, create_zone, zone_exist
from config             import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test






@pytest.fixture
def zone():
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = http://localhost:2633/RPC2
    """
    _id = create_zone(template)
    zone = Zone(_id)
    yield zone
    if not zone_exist(_id):
        return
    zone.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_not_exist(one: One):
    rename_if_not_exist__test(one.zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_zone(one: One, zone: Zone):
    rename__test(one.zone, zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_name_collision(one: One, zone: Zone):
    cant_be_renamed__test(one.zone, zone, Zone(0).info().NAME)
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_zone_name(one: One, zone: Zone):
    cant_be_renamed__test(one.zone, zone, "")



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_zone_name(one: One, zone: Zone, bad_symbol):
    cant_be_renamed__test(one.zone, zone, f"{bad_symbol}")
    cant_be_renamed__test(one.zone, zone, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.zone, zone, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.zone, zone, f"Greg{bad_symbol}Vetkin")
    
