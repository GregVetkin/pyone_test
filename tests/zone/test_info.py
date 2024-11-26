import pytest

from api                import One
from utils              import get_unic_name, run_command, federation_master, restart_opennebula
from one_cli.zone       import Zone, create_zone
from config             import ADMIN_NAME, API_URI, RAFT_CONFIG

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test




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
    info_if_not_exist__test(one.zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_info(one: One, zone: Zone):
    info__test(one.zone, zone)

