import pytest

from api                import One
from pyone              import OneNoExistsException, OneException
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
        NAME = {get_unic_name()}
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





def test_allocate_zone_by_xml():
    assert False, "Тест в разработке"



def test_required_attributes():
    assert False, "Тест в разработке"

    