import pytest
import random
from api                import One
from pyone              import OneNoExistsException


@pytest.fixture
def cluster_with_vnet(one: One, dummy_cluster, dummy_vnet):
    one.cluster.addvnet(dummy_cluster, dummy_vnet)
    yield dummy_cluster
    try:
        one.cluster.delvnet(dummy_cluster, dummy_vnet)
    except OneNoExistsException:
        pass
    


# =================================================================================================
# TESTS
# =================================================================================================



def test_cluster_not_exist(one: One, dummy_vnet):
    vnet_id = dummy_vnet
    with pytest.raises(OneNoExistsException):
        one.cluster.delvnet(999999, vnet_id)
   


def test_vnet_not_exist(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    with pytest.raises(OneNoExistsException):
        one.cluster.delvnet(cluster_id, 999999)
   


def test_remove_vnet_from_cluster(one: One, cluster_with_vnet):
    cluster_id              = cluster_with_vnet
    init_cluster_vnet_ids   = one.cluster.info(cluster_id).VNETS.ID
    target_vnet_id          = random.choice(init_cluster_vnet_ids)

    result = one.cluster.delvnet(cluster_id, target_vnet_id)
    assert result == cluster_id

    new_cluster_vnet_ids = one.cluster.info(cluster_id).VNETS.ID
    assert target_vnet_id not in new_cluster_vnet_ids
    assert len(new_cluster_vnet_ids) == len(init_cluster_vnet_ids) - 1
