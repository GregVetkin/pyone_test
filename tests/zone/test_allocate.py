import pytest

from api                import One
from pyone              import OneException
from utils.other        import get_unic_name
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn
from utils.opennebula   import federation_master, federation_standalone
from config.base        import API_URI




def run_command_via_ssh_as_local_admin(command: str):
    return run_command_via_ssh(local_admin_ssh_conn, command)


@pytest.fixture(scope="module")
def federation_master_mode():
    federation_master()
    yield
    federation_standalone()



# =================================================================================================
# TESTS
# =================================================================================================




def test_standalone_mode(one: One):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {API_URI}
     """
    with pytest.raises(OneException):
        one.zone.allocate(template)





def test_allocate_zone(one: One, federation_master_mode):
    name     = get_unic_name()
    endpoint = API_URI
    template = f"""
        NAME = {name}
        ENDPOINT = {endpoint}
     """
    
    zone_id  = one.zone.allocate(template)

    assert zone_id in [zone.ID for zone in one.zonepool.info().ZONE]
    zone_info = one.zone.info(zone_id, False)
    
    assert zone_info.NAME == name
    assert zone_info.TEMPLATE["ENDPOINT"] == endpoint

    one.zone.delete(zone_id)





def test_allocate_by_xml(one: One, federation_master_mode):
    name     = get_unic_name()
    endpoint = API_URI
    template = f"<ZONE><NAME>{name}</NAME><ENDPOINT>{endpoint}</ENDPOINT></ZONE>"
    
    zone_id  = one.zone.allocate(template)

    assert zone_id in [zone.ID for zone in one.zonepool.info().ZONE]
    zone_info = one.zone.info(zone_id, False)
    
    assert zone_info.NAME == name
    assert zone_info.TEMPLATE["ENDPOINT"] == endpoint

    one.zone.delete(zone_id)





def test_name_is_mandatory(one: One, federation_master_mode):
    template = f"ENDPOINT={API_URI}"
    with pytest.raises(OneException):
        one.zone.allocate(template)
    



def test_endpoint_is_mandatory(one: One, federation_master_mode):
    template = f"NAME={get_unic_name()}"
    with pytest.raises(OneException):
        one.zone.allocate(template)

