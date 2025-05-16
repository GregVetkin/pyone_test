import pytest
import random
import pyone
from api    import One




@pytest.fixture
def cluster_with_host(one: One, dummy_cluster, dummy_host):
    one.cluster.addhost(dummy_cluster, dummy_host)
    yield dummy_cluster
    try:
        one.cluster.delhost(dummy_cluster, dummy_host)
    except pyone.OneNoExistsException:
        pass
    








def test_cluster_not_exist(one: One, dummy_host):
    host_id = dummy_host
    with pytest.raises(pyone.OneNoExistsException):
        one.cluster.delhost(999999, host_id)
   


def test_host_not_exist(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    with pytest.raises(pyone.OneNoExistsException):
        one.cluster.delhost(cluster_id, 999999)
   


def test_remove_host_from_cluster(one: One, cluster_with_host):
    cluster_id       = cluster_with_host
    cluster_host_ids = one.cluster.info(cluster_id).HOSTS.ID
    target_host_id   = random.choice(cluster_host_ids)

    result = one.cluster.delhost(cluster_id, target_host_id)
    assert result == cluster_id

    new_cluster_host_ids = one.cluster.info(cluster_id).HOSTS.ID
    assert target_host_id not in new_cluster_host_ids
    assert len(new_cluster_host_ids) == len(cluster_host_ids) - 1
