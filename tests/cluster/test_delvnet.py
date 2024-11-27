import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster, cluster_exist
from one_cli.vnet       import Vnet, vnet_exist, create_vnet
from config             import ADMIN_NAME



@pytest.fixture
def cluster():
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    yield cluster
    if cluster_exist(cluster_id):
        cluster.delete()
    

@pytest.fixture
def vnet():
    vnet_template = f"""
        NAME   = {get_unic_name()}
        VN_MAD = bridge
    """
    vnet_id = create_vnet(vnet_template)
    vnet    = Vnet(vnet_id)
    yield vnet
    vnet.delete()


@pytest.fixture
def cluster_with_vnet(vnet):
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    cluster.addvnet(vnet._id)
    yield cluster
    if cluster_exist(cluster_id):
        cluster.delvnet(vnet._id)
        cluster.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One, vnet: Vnet):
    with pytest.raises(OneException):
        one.cluster.delvnet(999999, vnet._id)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vnet_not_exist(one: One, cluster: Cluster):
    with pytest.raises(OneException):
        one.cluster.delvnet(cluster._id, 999999)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_remove_vnet_from_cluster(one: One, cluster_with_vnet: Cluster):
    old_cluster_vnets = cluster_with_vnet.info().VNETS
    assert old_cluster_vnets
    vnet_id = old_cluster_vnets[0]

    _id = one.cluster.delvnet(cluster_with_vnet._id, vnet_id)
    assert _id == cluster_with_vnet._id

    new_cluster_vnets = cluster_with_vnet.info().VNETS
    assert vnet_id not in new_cluster_vnets
    assert len(new_cluster_vnets) == len(old_cluster_vnets) - 1
