import pytest

from api    import One
from pyone  import OneNoExistsException





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
        one.cluster.addvnet(999999, vnet_id)
   


def test_vnet_not_exist(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    with pytest.raises(OneNoExistsException):
        one.cluster.addvnet(cluster_id, 999999)
   


def test_add_vnet_to_cluster(one: One, dummy_cluster, dummy_vnet):
    cluster_id, vnet_id = dummy_cluster, dummy_vnet

    result = one.cluster.addvnet(cluster_id, vnet_id)
    assert result == cluster_id
    assert vnet_id in one.cluster.info(cluster_id).VNETS.ID



def test_add_already_added_vnet(one: One, cluster_with_vnet):
    cluster_id             = cluster_with_vnet
    init_cluster_vnet_ids  = one.cluster.info(cluster_id).VNETS.ID
    added_vnet_id          = init_cluster_vnet_ids[-1]

    result = one.cluster.addvnet(cluster_id, added_vnet_id)
    assert result == cluster_id

    new_cluster_vnet_ids = one.cluster.info(cluster_id).VNETS.ID
    assert added_vnet_id in new_cluster_vnet_ids
    assert len(init_cluster_vnet_ids) == len(new_cluster_vnet_ids)
