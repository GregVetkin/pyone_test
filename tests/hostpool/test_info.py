import pytest
from api            import One
from utils.other    import get_unic_name



@pytest.fixture
def host_ids(one: One):
    host_ids_list = []
    for _ in range(5):
        host_name = get_unic_name()
        host_id   = one.host.allocate(host_name)
        host_ids_list.append(host_id)

    yield host_ids_list

    for host_id in host_ids_list:
        one.host.delete(host_id)




# =================================================================================================
# TESTS
# =================================================================================================



def test_show_all_hosts(one: One, host_ids):
    hostpool_ids = [host.ID for host in one.hostpool.info().HOST]
    assert set(host_ids).issubset(hostpool_ids)

