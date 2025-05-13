import pytest
import random
from api       import One
from pyone     import OneNoExistsException




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



def test_cluster_not_exist(one: One, dummy_datastore):
    with pytest.raises(OneNoExistsException):
        one.cluster.deldatastore(999999, dummy_datastore)
   

def test_datastore_not_exist(one: One, dummy_cluster):
    with pytest.raises(OneNoExistsException):
        one.cluster.deldatastore(dummy_cluster, 999999)
   

def test_remove_datastore_from_cluster(one: One, cluster_with_datastore):
    cluster_id                  = cluster_with_datastore
    init_cluster_datastore_ids  = one.cluster.info(cluster_id).DATASTORES.ID
    target_datastore_id         = random.choice(init_cluster_datastore_ids)

    result = one.cluster.deldatastore(cluster_id, target_datastore_id)
    assert result == cluster_id

    new_cluster_datastore_ids = one.cluster.info(cluster_id).DATASTORES.ID
    assert target_datastore_id not in new_cluster_datastore_ids
    assert len(new_cluster_datastore_ids) == len(init_cluster_datastore_ids) - 1

