import pytest
from api            import One
from utils.other    import get_unic_name



@pytest.fixture
def host_ids(one: One):
    host_ids_list = [one.host.allocate(get_unic_name(), "kvm", "kvm", -1) for _ in range(5)]

    yield host_ids_list

    for host_id in host_ids_list:
        one.host.delete(host_id)







def test_get_all_hosts_info(one: One, host_ids):
    hostpool_ids = [host.ID for host in one.hostpool.info().HOST]
    assert set(host_ids).issubset(hostpool_ids)

