import pytest
from api                import One
from utils.other        import get_unic_name
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn
from utils.opennebula   import federation_master, federation_standalone
from config.base        import API_URI, RAFT_ENABLED

from tests._common_methods.info     import info__test, not_exist__test




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
    one.zone.delete(zone_id)



# =================================================================================================
# TESTS
# =================================================================================================



def test_zone_not_exist(one: One):
    not_exist__test(one.zone)


@pytest.mark.skipif(RAFT_ENABLED is True, 
                    reason="Test for ONE_SERVER scenario only"
                    )
def test_zone_info(one: One, dummy_zone: int):
    zone_id = dummy_zone
    info__test(one.zone, zone_id)


