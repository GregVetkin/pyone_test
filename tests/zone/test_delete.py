import pytest
import time

from api                import One
from utils              import get_unic_name
from one_cli.zone       import Zone, create_zone, zone_exist
from config             import ADMIN_NAME, API_URI

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test



@pytest.mark.parametrize("federation_mode", ["MASTER"], indirect=True)
@pytest.fixture
def zone(federation_mode):
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = {API_URI}
    """
    _id = create_zone(template)
    zone = Zone(_id)
    yield zone
    if not zone_exist(_id):
        return
    zone.delete()







# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_not_exist(one: One):
    delete_if_not_exist__test(one.zone)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_zone(one: One,  zone: Zone):
    delete__test(one.zone, zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_system_zone(one: One):
    cant_be_deleted__test(one.zone, Zone(0))

