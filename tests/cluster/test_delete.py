import pytest

from pyone                          import OneNoExistsException, OneActionException
from api                            import One

from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import not_exist__test



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







def test_cluster_not_exist(one: One):
   not_exist__test(one.cluster)
   


def test_delete_cluster(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    delete__test(one.cluster, cluster_id)



def test_cant_delete_default_cluster(one: One):
    cluster_id = 0

    with pytest.raises(OneActionException):
        delete__test(one.cluster, cluster_id)


def test_cant_delete_cluster_with_host(one: One, cluster_with_host):
    cluster_id = cluster_with_host
    
    with pytest.raises(OneActionException):
        delete__test(one.cluster, cluster_id)


def test_cant_delete_cluster_with_datastore(one: One, cluster_with_datastore):
    cluster_id = cluster_with_datastore
    
    with pytest.raises(OneActionException):
        delete__test(one.cluster, cluster_id)


def test_cant_delete_cluster_with_vnet(one: One, cluster_with_vnet):
    cluster_id = cluster_with_vnet
    
    with pytest.raises(OneActionException):
        delete__test(one.cluster, cluster_id)
