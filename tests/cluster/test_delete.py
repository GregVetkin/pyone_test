import pytest

from api                            import One
from pyone                          import OneNoExistsException
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test


@pytest.fixture
def cluster_with_host(one: One, dummy_cluster, dummy_host):
    one.cluster.addhost(dummy_cluster, dummy_host)
    yield dummy_cluster
    try:
        one.cluster.delhost(dummy_cluster, dummy_host)
    except OneNoExistsException:
        pass
    

@pytest.fixture
def cluster_with_vnet(one: One, dummy_cluster, dummy_vnet):
    one.cluster.addvnet(dummy_cluster, dummy_vnet)
    yield dummy_cluster
    try:
        one.cluster.delvnet(dummy_cluster, dummy_vnet)
    except OneNoExistsException:
        pass
    

@pytest.fixture
def cluster_with_datastore(one: One, dummy_datastore, dummy_cluster):
    one.cluster.adddatastore(dummy_cluster, dummy_datastore)
    yield dummy_cluster
    try:
        one.cluster.deldatastore(dummy_cluster, dummy_datastore)
    except OneNoExistsException:
        pass





# =================================================================================================
# TESTS
# =================================================================================================



def test_cluster_not_exist(one: One):
   delete_if_not_exist__test(one.cluster)
   


def test_delete_empty_cluster(one: One, dummy_cluster):
    cluster_id   = dummy_cluster
    cluster_info = one.cluster.info(cluster_id)
    assert not cluster_info.DATASTORES.ID
    assert not cluster_info.HOSTS.ID
    assert not cluster_info.VNETS.ID
    delete__test(one.cluster, dummy_cluster)



def test_cant_delete_default_cluster(one: One):
    cant_be_deleted__test(one.cluster, 0)



def test_cant_delete_cluster_with_host(one: One, cluster_with_host):
    cluster_id = cluster_with_host
    assert one.cluster.info(cluster_id).HOSTS.ID
    cant_be_deleted__test(one.cluster, cluster_id)



def test_cant_delete_cluster_with_datastore(one: One, cluster_with_datastore):
    cluster_id = cluster_with_datastore
    assert one.cluster.info(cluster_id).DATASTORES.ID
    cant_be_deleted__test(one.cluster, cluster_id)



def test_cant_delete_cluster_with_vnet(one: One, cluster_with_vnet):
    cluster_id = cluster_with_vnet
    assert one.cluster.info(cluster_id).VNETS.ID
    cant_be_deleted__test(one.cluster, cluster_id)
