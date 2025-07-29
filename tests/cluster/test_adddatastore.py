import pytest
import random

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





def test_cluster_not_exist(one: One, dummy_datastore):
    cluster_id   = random.randint(9999, 999999)
    datastore_id = dummy_datastore

    with pytest.raises(OneNoExistsException):
        one.cluster.adddatastore(cluster_id, datastore_id)



def test_datastore_not_exist(one: One, dummy_cluster):
    cluster_id   = dummy_cluster
    datastore_id = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        one.cluster.adddatastore(cluster_id, datastore_id)
   


def test_add_datastore(one: One, dummy_cluster, dummy_datastore):
    cluster_id   = dummy_cluster
    datastore_id = dummy_datastore

    _id = one.cluster.adddatastore(cluster_id, datastore_id)

    assert _id == cluster_id
    assert datastore_id in one.cluster.info(cluster_id, False).DATASTORES.ID



def test_add_added_datastore(one: One, cluster_with_datastore):
    cluster_id            = cluster_with_datastore
    cluster_datastore_ids = one.cluster.info(cluster_id, False).DATASTORES.ID
    added_datastore_id    = cluster_datastore_ids[-1]

    result = one.cluster.adddatastore(cluster_id, added_datastore_id)
    assert result == cluster_id

    new_cluster_datastore_ids = one.cluster.info(cluster_id, False).DATASTORES.ID
    assert added_datastore_id in new_cluster_datastore_ids
    assert len(cluster_datastore_ids) == len(new_cluster_datastore_ids)
