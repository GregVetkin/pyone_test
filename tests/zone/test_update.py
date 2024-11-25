import pytest

from api                import One
from utils              import get_unic_name
from one_cli.zone       import Zone, create_zone, zone_exist
from config             import ADMIN_NAME

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test





@pytest.fixture
def zone():
    template = f"""
        NAME     = {get_unic_name()}
        ENDPOINT = http://localhost:2633/RPC2
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
    update_if_not_exist__test(one.zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_zone__replace(one: One, zone: Zone):
    update_and_replace__test(one.zone, zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_zone__merge(one: One, zone: Zone):
    update_and_merge__test(one.zone, zone)




