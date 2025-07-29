import pytest
import random

from api    import One
from pyone  import OneNoExistsException, OneException





@pytest.fixture
def cluster_with_vnet(one: One, dummy_cluster, dummy_vnet):
    one.cluster.addvnet(dummy_cluster, dummy_vnet)
    yield dummy_cluster
    try:
        one.cluster.delvnet(dummy_cluster, dummy_vnet)
    except OneException:
        pass
    





def test_cluster_not_exist(one: One, dummy_vnet):
    cluster_id  = random.randint(9999, 999999)
    vnet_id     = dummy_vnet

    with pytest.raises(OneNoExistsException):
        one.cluster.delvnet(cluster_id, vnet_id)
   


def test_vnet_not_exist(one: One, dummy_cluster):
    cluster_id  = dummy_cluster
    vnet_id     = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        one.cluster.delvnet(cluster_id, vnet_id)
   


def test_remove_vnet_from_cluster(one: One, cluster_with_vnet):
    cluster_id       = cluster_with_vnet
    cluster_vnet_ids = one.cluster.info(cluster_id, False).VNETS.ID
    target_vnet_id   = random.choice(cluster_vnet_ids)

    result = one.cluster.delvnet(cluster_id, target_vnet_id)
    assert result == cluster_id

    new_cluster_vnet_ids = one.cluster.info(cluster_id, False).VNETS.ID
    assert target_vnet_id not in new_cluster_vnet_ids
    assert len(new_cluster_vnet_ids) == len(cluster_vnet_ids) - 1
