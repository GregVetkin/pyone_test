import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster, cluster_exist
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME




@pytest.fixture
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



@pytest.fixture
def cluster():
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    yield cluster
    cluster.delete()



@pytest.fixture
def cluster_with_datastore(datastore):
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    cluster.adddatastore(datastore._id)
    yield cluster
    cluster.deldatastore(datastore._id)
    cluster.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One, datastore: Datastore):
    with pytest.raises(OneException):
        one.cluster.adddatastore(999999, datastore._id)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One, cluster: Cluster):
    with pytest.raises(OneException):
        one.cluster.adddatastore(cluster._id, 999999)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_add_datastore_to_cluster(one: One, cluster: Cluster, datastore: Datastore):
    assert datastore._id not in cluster.info().DATASTORES
    _id = one.cluster.adddatastore(cluster._id, datastore._id)
    assert _id == cluster._id
    assert datastore._id in cluster.info().DATASTORES


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_add_added_datastore_to_cluster(one: One, cluster_with_datastore: Cluster):
    old_cluster_datastores = cluster_with_datastore.info().DATASTORES
    assert old_cluster_datastores
    added_datastore_id = old_cluster_datastores[0]

    _id = one.cluster.adddatastore(cluster_with_datastore._id, added_datastore_id)
    assert _id == cluster_with_datastore._id

    new_cluster_datastores = cluster_with_datastore.info().DATASTORES
    assert added_datastore_id in new_cluster_datastores
    assert len(old_cluster_datastores) == len(new_cluster_datastores)
