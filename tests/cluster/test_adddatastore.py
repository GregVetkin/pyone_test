import pytest

from api    import One
from pyone  import OneNoExistsException




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
        one.cluster.adddatastore(999999, dummy_datastore)
   

def test_datastore_not_exist(one: One, dummy_cluster):
    with pytest.raises(OneNoExistsException):
        one.cluster.adddatastore(dummy_cluster, 999999)
   

def test_add_datastore_to_cluster(one: One, dummy_cluster, dummy_datastore):
    cluster_id, datastore_id = dummy_cluster, dummy_datastore
    assert datastore_id not in one.cluster.info(cluster_id).DATASTORES.ID
    result = one.cluster.adddatastore(cluster_id, datastore_id)
    assert result == cluster_id
    assert datastore_id in one.cluster.info(cluster_id).DATASTORES.ID



def test_add_already_added_datastore(one: One, cluster_with_datastore):
    cluster_id                  = cluster_with_datastore
    init_cluster_datastore_ids  = one.cluster.info(cluster_id).DATASTORES.ID
    added_datastore_id          = init_cluster_datastore_ids[-1]

    result = one.cluster.adddatastore(cluster_id, added_datastore_id)
    assert result == cluster_id

    new_cluster_datastore_ids = one.cluster.info(cluster_id).DATASTORES.ID
    assert added_datastore_id in new_cluster_datastore_ids
    assert len(init_cluster_datastore_ids) == len(new_cluster_datastore_ids)
