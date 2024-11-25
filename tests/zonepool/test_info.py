import pytest

from api                import One
from utils              import get_unic_name
from one_cli.zone       import Zone, create_zone
from config             import ADMIN_NAME, API_URI
from typing             import List






@pytest.fixture
def zones():
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

