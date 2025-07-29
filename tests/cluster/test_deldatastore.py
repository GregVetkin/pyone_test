import pytest
import random

from api    import One
from pyone  import OneNoExistsException, OneException




@pytest.fixture
def cluster_with_datastore(one: One, dummy_datastore, dummy_cluster):
    one.cluster.adddatastore(dummy_cluster, dummy_datastore)
    yield dummy_cluster
    try:
        one.cluster.deldatastore(dummy_cluster, dummy_datastore)
    except OneException:
        pass






def test_cluster_not_exist(one: One, dummy_datastore):
    cluster_id   = random.randint(9999, 999999)
    datastore_id = dummy_datastore

    with pytest.raises(OneNoExistsException):
        one.cluster.deldatastore(cluster_id, datastore_id)
   

def test_datastore_not_exist(one: One, dummy_cluster):
    cluster_id   = dummy_cluster
    datastore_id = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        one.cluster.deldatastore(cluster_id, datastore_id)
   


def test_delete_datastore_from_cluster(one: One, cluster_with_datastore):
    cluster_id            = cluster_with_datastore
    cluster_datastore_ids = one.cluster.info(cluster_id, False).DATASTORES.ID
    target_datastore_id   = random.choice(cluster_datastore_ids)

    _id = one.cluster.deldatastore(cluster_id, target_datastore_id)
    assert _id == cluster_id

    new_cluster_datastore_ids = one.cluster.info(cluster_id, False).DATASTORES.ID
    assert target_datastore_id not in new_cluster_datastore_ids
    assert len(new_cluster_datastore_ids) == len(cluster_datastore_ids) - 1

