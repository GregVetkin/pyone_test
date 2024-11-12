import pytest

from api                import One
from utils              import get_user_auth
from one_cli.host       import Host, create_host
from config             import BRESTADM
from typing             import List


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def hosts(one: One):
    host_list = []
    for _ in range(5):
        host_name = f"api_test_host_{_}"
        host_id   = one.host.allocate(host_name)
        host      = Host(host_id)
        host_list.append(host)

    yield host_list

    for host in host_list:
        host.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_show_all_hosts(one: One, hosts: List[Host]):
    host_ids     = [host.info().ID for host in hosts]
    hostpool     = one.hostpool.info().HOST
    hostpool_ids = [host.ID for host in hostpool]
    assert set(host_ids).issubset(hostpool_ids)

