import pytest
import time
from api                import One
from utils.other        import get_unic_name
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn
from utils.opennebula   import federation_master, federation_standalone
from config.base        import API_URI


from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test



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
    delete_if_not_exist__test(one.zone)




def test_delete_zone(one: One,  dummy_zone: int):
    zone_id = dummy_zone
    delete__test(one.zone, zone_id)



def test_delete_system_zone_0(one: One):
    zone_id = 0
    cant_be_deleted__test(one.zone, zone_id)

