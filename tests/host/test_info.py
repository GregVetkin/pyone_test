import pytest

from api                import One
from utils              import get_unic_name
from one_cli.host       import Host, create_host, host_exist
from config             import ADMIN_NAME

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test




@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(f"{get_unic_name()}")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()
    


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One):
    info_if_not_exist__test(one.host)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_info(one: One, host: Host):
    info__test(one.host, host)
