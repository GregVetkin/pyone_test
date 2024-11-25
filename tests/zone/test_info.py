import pytest

from api                import One
from utils              import get_unic_name
from one_cli.zone       import Zone, create_zone, zone_exist
from config             import ADMIN_NAME

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test




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
    info_if_not_exist__test(one.zone)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_info(one: One, zone: Zone):
    info__test(one.zone, zone)

