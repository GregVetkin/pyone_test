import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name, federation_master, restart_opennebula, run_command
from one_cli.zone       import Zone, zone_exist
from config             import ADMIN_NAME, API_URI, RAFT_CONFIG




@pytest.fixture(scope="module")
def federation_master_mode():
    copy_path  = "/tmp/raft_orig.conf"
    run_command(f"sudo cp -p {RAFT_CONFIG} {copy_path}")
    federation_master()
    yield
    run_command(f"sudo cat {copy_path} | sudo tee {RAFT_CONFIG}")
    run_command(f"sudo rm -f {copy_path}")
    restart_opennebula()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("federation_mode", ["STANDALONE"], indirect=True)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_not_a_master_mode(one: One, federation_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {API_URI}
     """
    with pytest.raises(OneException):
        one.zone.allocate(template)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_zone(one: One, federation_master_mode):
    template = f"""
        NAME = {get_unic_name()}
        ENDPOINT = {API_URI}
     """
    zone_id = one.zone.allocate(template)
    assert zone_exist(zone_id)
    Zone(zone_id).delete()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_zone_by_xml(one: One, federation_master_mode):
    template = f"<ZONE><NAME>{get_unic_name()}</NAME><ENDPOINT>{API_URI}</ENDPOINT></ZONE>"
    zone_id  = one.zone.allocate(template)
    assert zone_exist(zone_id)
    Zone(zone_id).delete()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_required_attributes(one: One, federation_master_mode):

    template_without_name = f"ENDPOINT={API_URI}"
    with pytest.raises(OneException):
        one.zone.allocate(template_without_name)
    
    template_without_endpoint = f"NAME={get_unic_name()}"
    with pytest.raises(OneException):
        one.zone.allocate(template_without_endpoint)

