import pytest
import random

from api    import One
from pyone  import OneNoExistsException, OneException




@pytest.fixture
def cluster_with_host(one: One, dummy_cluster, dummy_host):
    one.cluster.addhost(dummy_cluster, dummy_host)
    yield dummy_cluster
    try:
        one.cluster.delhost(dummy_cluster, dummy_host)
    except OneException:
        pass
    




def test_cluster_not_exist(one: One, dummy_host):
    cluster_id  = random.randint(9999, 999999)
    host_id     = dummy_host

    with pytest.raises(OneNoExistsException):
        one.cluster.addhost(cluster_id, host_id)
   


def test_host_not_exist(one: One, dummy_cluster):
    cluster_id  = dummy_cluster
    host_id     = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        one.cluster.addhost(cluster_id, host_id)
   


def test_add_host(one: One, dummy_cluster, dummy_host):
    cluster_id, host_id = dummy_cluster, dummy_host

    assert host_id not in one.cluster.info(cluster_id, False).HOSTS.ID
    result = one.cluster.addhost(cluster_id, host_id)
    assert result == cluster_id
    assert host_id in one.cluster.info(cluster_id, False).HOSTS.ID



def test_add_added_host(one: One, cluster_with_host):
    cluster_id       = cluster_with_host
    cluster_host_ids = one.cluster.info(cluster_id, False).HOSTS.ID
    added_host_id    = cluster_host_ids[-1]

    result = one.cluster.addhost(cluster_id, added_host_id)
    assert result == cluster_id

    new_cluster_host_ids = one.cluster.info(cluster_id, False).HOSTS.ID
    assert added_host_id in new_cluster_host_ids
    assert len(cluster_host_ids) == len(new_cluster_host_ids)
