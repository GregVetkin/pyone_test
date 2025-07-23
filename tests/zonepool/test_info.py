import pytest
import random
from api                import One
from utils.other        import get_unic_name, wait_until
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn

from config.base        import API_URI, RAFT_CONFIG
from typing             import List



def run_command_via_ssh_as_local_admin(command: str):
    return run_command_via_ssh(local_admin_ssh_conn, command)




@pytest.fixture(scope="module")
def federation_master_mode():
    copy_path  = "/tmp/raft_orig.conf"
    run_command_via_ssh(f"sudo cp -p {RAFT_CONFIG} {copy_path}")

    federation_master()
    yield

    run_command_via_ssh_as_local_admin(f"sudo cat {copy_path} | sudo tee {RAFT_CONFIG}")
    run_command_via_ssh_as_local_admin(f"sudo rm -f {copy_path}")
    run_command_via_ssh_as_local_admin("sudo systemctl restart opennebula")




@pytest.fixture
def zones(one: One, federation_master_mode):
    zone_ids = []

    for _ in range(random.randint(5, 10)):
        template = f"""
            NAME     = {get_unic_name()}
            ENDPOINT = {API_URI}
        """
        zone_id = one.zone.allocate(template)
        zone_ids.append(zone_id)

    yield zone_ids

    for zone_id in zone_ids:
        one.zone.delete(zone_id)

    wait_until(
        lambda: set(zone_ids).isdisjoint(set([zone.ID for zone in one.zonepool.info().IMAGE]))
    )
    



# =================================================================================================
# TESTS
# =================================================================================================



def test_show_all_zones(one: One, zones: List[int]):
    created_zone_ids = zones
    all_zone_ids     = [zone.ID for zone in one.zonepool.info().ZONEool]
    assert set(created_zone_ids).issubset(all_zone_ids)

