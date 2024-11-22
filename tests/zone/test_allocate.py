import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.zone       import Zone, zone_exist
from config             import ADMIN_NAME




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("federation_mode", ["STANDALONE"], indirect=True)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_not_a_master_mode(one: One, federation_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {Zone(0).info().TEMPLATE["ENDPOINT"]}
     """
    with pytest.raises(OneException):
        one.zone.allocate(template)



@pytest.mark.parametrize("federation_mode", ["MASTER"], indirect=True)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_zone(one: One, federation_mode):
    template = f"""
        NAME = {get_unic_name()}
        ENDPOINT = {Zone(0).info().TEMPLATE["ENDPOINT"]}
     """
    zone_id = one.zone.allocate(template)
    assert zone_exist(zone_id)
    Zone(zone_id).delete()



@pytest.mark.parametrize("federation_mode", ["MASTER"], indirect=True)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_zone_by_xml(one: One, federation_mode):
    name = get_unic_name()
    endpoint = Zone(0).info().TEMPLATE["ENDPOINT"]
    template = f"<ZONE><NAME>{name}</NAME><ENDPOINT>{endpoint}</ENDPOINT></ZONE>"
    zone_id = one.zone.allocate(template)
    assert zone_exist(zone_id)
    Zone(zone_id).delete()



@pytest.mark.parametrize("federation_mode", ["MASTER"], indirect=True)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_required_attributes(one: One, federation_mode):
    name = get_unic_name()
    endp = Zone(0).info().TEMPLATE["ENDPOINT"]

    template_without_name = f"ENDPOINT={endp}"
    with pytest.raises(OneException):
        one.zone.allocate(template_without_name)
    
    template_without_endpoint = f"NAME={name}"
    with pytest.raises(OneException):
        one.zone.allocate(template_without_endpoint)

