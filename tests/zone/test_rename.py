import pytest
from api                import One
from utils.other        import get_unic_name
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn
from utils.opennebula   import federation_master, federation_standalone
from config.base        import API_URI
from config.tests       import INVALID_CHARS

from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test





def run_command_via_ssh_as_local_admin(command: str):
    return run_command_via_ssh(local_admin_ssh_conn, command)


@pytest.fixture(scope="module")
def federation_master_mode():
    federation_master()
    yield
    federation_standalone()


@pytest.fixture
def dummy_zone(one: One, federation_master_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {API_URI}
    """
    zone_id = one.zone.allocate(template)
    
    yield zone_id

    if zone_id in [zone.ID for zone in one.zonepool.info().ZONE]:
        one.zone.delete(zone_id)




# =================================================================================================
# TESTS
# =================================================================================================




def test_zone_not_exist(one: One):
    not_exist__test(one.zone)




def test_rename(one: One, dummy_zone: int):
    zone_id = dummy_zone
    rename__test(one.zone, zone_id)




def test_name_collision(one: One, dummy_zone: int):
    zone_id  = dummy_zone
    new_name = one.zone.info(0).NAME
    cant_be_renamed__test(one.zone, zone_id, new_name)
    



def test_empty_name(one: One, dummy_zone: int):
    zone_id  = dummy_zone
    new_name = ""
    cant_be_renamed__test(one.zone, zone_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_zone: int, char: str):
    zone_id = dummy_zone

    cant_be_renamed__test(one.zone, zone_id, f"{char}")
    cant_be_renamed__test(one.zone, zone_id, f"Greg{char}")
    cant_be_renamed__test(one.zone, zone_id, f"{char}Vetkin")
    cant_be_renamed__test(one.zone, zone_id, f"Greg{char}Vetkin")
    
