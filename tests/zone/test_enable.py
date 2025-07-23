import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils.other        import get_unic_name
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn
from utils.opennebula   import federation_master, federation_standalone




def run_command_via_ssh_as_local_admin(command: str):
    return run_command_via_ssh(local_admin_ssh_conn, command)


@pytest.fixture(scope="module")
def federation_master_mode():
    federation_master()
    yield
    federation_standalone()


@pytest.fixture
def zone_with_different_endpoint(one: One, federation_master_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = "http://spam.eggs:2633/RPC2"
    """
    zone_id = one.zone.allocate(template)

    yield zone_id

    if zone_id in [zone.ID for zone in one.zonepool.info().ZONE]:
        one.zone.delete(zone_id)




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("enable", [True, False])
def test_zone_not_exist(one: One, enable: bool):
    zone_id = 99999
    with pytest.raises(OneNoExistsException):
        one.zone.enable(zone_id, enable)



@pytest.mark.parametrize("enable", [True, False])
def test_enable_system_zone_0(one: One, enable: bool):
    zone_id = 0
    _id     = one.zone.enable(zone_id, enable)

    assert _id == zone_id
    
    if enable:
        assert one.zone.info(zone_id).STATE == 0
    else:
        assert one.zone.info(zone_id).STATE == 1

    one.zone.enable(zone_id, True)
    assert one.zone.info(zone_id).STATE == 0
    




@pytest.mark.parametrize("enable", [True, False])
def test_different_endpoint(one: One, zone_with_different_endpoint: int, enable: bool):
    zone_id = zone_with_different_endpoint
    zone_state_brefore = one.zone.info(zone_id).STATE
    
    with pytest.raises(OneActionException):
        one.zone.enable(zone_id, enable)

    zone_state_after = one.zone.info(zone_id).STATE
    assert zone_state_brefore == zone_state_after




