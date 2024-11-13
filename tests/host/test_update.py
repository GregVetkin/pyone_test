import pytest

from api             import One
from utils           import get_user_auth
from one_cli.host    import Host, create_host, host_exist
from config          import BRESTADM

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_update")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_not_exist(one: One):
    update_if_not_exist__test(one.host)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_host__replace(one: One, host: Host):
    update_and_replace__test(one.host, host)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_host__merge(one: One, host: Host):
    update_and_merge__test(one.host, host)
