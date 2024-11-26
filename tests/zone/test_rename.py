import pytest
from api                import One
from utils              import get_unic_name, restart_opennebula, federation_master, run_command
from one_cli.zone       import Zone, create_zone
from config             import ADMIN_NAME, BAD_SYMBOLS, API_URI, RAFT_CONFIG

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test



@pytest.fixture(scope="module")
def federation_master_mode():
    copy_path  = "/tmp/raft_orig.conf"
    run_command(f"sudo cp -p {RAFT_CONFIG} {copy_path}")
    federation_master()
    yield
    run_command(f"sudo cat {copy_path} | sudo tee {RAFT_CONFIG}")
    run_command(f"sudo rm -f {copy_path}")
    restart_opennebula()


@pytest.fixture
def zone(federation_master_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {API_URI}
    """
    _id = create_zone(template)
    zone = Zone(_id)
    yield zone
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
    
