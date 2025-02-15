import pytest

from api             import One
from utils           import get_unic_name
from one_cli.host    import Host, create_host, host_exist
from config          import ADMIN_NAME

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test



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
    update_if_not_exist__test(one.host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_host__replace(one: One, host: Host):
    update_and_replace__test(one.host, host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_host__merge(one: One, host: Host):
    update_and_merge__test(one.host, host)
