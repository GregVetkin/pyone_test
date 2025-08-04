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
        one.cluster.addvnet(cluster_id, vnet_id)
   


def test_vnet_not_exist(one: One, dummy_cluster):
    cluster_id  = dummy_cluster
    vnet_id     = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        one.cluster.addvnet(cluster_id, vnet_id)
   


def test_add_vnet(one: One, dummy_cluster, dummy_vnet):
    cluster_id, vnet_id = dummy_cluster, dummy_vnet

    result = one.cluster.addvnet(cluster_id, vnet_id)
    assert result == cluster_id
    assert vnet_id in one.cluster.info(cluster_id, False).VNETS.ID



def test_add_added_vnet(one: One, cluster_with_vnet):
    cluster_id       = cluster_with_vnet
    cluster_vnet_ids = one.cluster.info(cluster_id, False).VNETS.ID
    added_vnet_id    = cluster_vnet_ids[-1]

    result = one.cluster.addvnet(cluster_id, added_vnet_id)
    assert result == cluster_id

    new_cluster_vnet_ids = one.cluster.info(cluster_id, False).VNETS.ID
    assert added_vnet_id in new_cluster_vnet_ids
    assert len(cluster_vnet_ids) == len(new_cluster_vnet_ids)
