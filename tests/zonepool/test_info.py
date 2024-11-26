import pytest

from api                import One
from utils              import get_unic_name, restart_opennebula, federation_master, run_command
from one_cli.zone       import Zone, create_zone
from config             import ADMIN_NAME, API_URI, RAFT_CONFIG
from typing             import List



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
def zones(federation_master_mode):
    zone_list = []
    for _ in range(5):
        template = f"""
            NAME     = {get_unic_name()}
            ENDPOINT = {API_URI}
        """
        zone_id = create_zone(template)
        zone    = Zone(zone_id)
        zone_list.append(zone)

    yield zone_list

    for zone in zone_list:
        zone.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_show_all_zones(one: One, zones: List[Zone]):
    zone_ids       = [zone.info().ID for zone in zones]
    zonepool       = one.zonepool.info().ZONE
    zonepool_ids   = [zone.ID for zone in zonepool]
    
    assert set(zone_ids).issubset(zonepool_ids)

