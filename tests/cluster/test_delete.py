import pytest

from api                import One
from utils              import get_unic_name
from one_cli.host       import Host, create_host
from one_cli.cluster    import Cluster, create_cluster, cluster_exist
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vnet       import Vnet, vnet_exist, create_vnet
from config             import ADMIN_NAME

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test



@pytest.fixture
def empty_cluster():
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    yield cluster
    if cluster_exist(cluster_id):
        cluster.delete()
    

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
def cluster_with_datastore(datastore):
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    cluster.adddatastore(datastore._id)
    yield cluster

    try:
        cluster.deldatastore(datastore._id)
        cluster.delete()
    except Exception:
        pass


@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(hostname=get_unic_name())
    host    = Host(host_id)
    yield host
    host.delete()


@pytest.fixture
def cluster_with_host(host):
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    cluster.addhost(host._id)
    yield cluster

    try:
        cluster.delhost(host._id)
        cluster.delete()
    except Exception:
        pass




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
    try:
        cluster.delvnet(vnet._id)
        cluster.delete()
    except Exception:
        pass




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One):
   delete_if_not_exist__test(one.cluster)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_empty_cluster(one: One, empty_cluster: Cluster):
    assert not empty_cluster.info().DATASTORES
    assert not empty_cluster.info().HOSTS
    assert not empty_cluster.info().VNETS
    delete__test(one.cluster, empty_cluster)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_system_cluster(one: One):
    cant_be_deleted__test(one.cluster, Cluster(0))


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_cluster_with_host(one: One, cluster_with_host: Cluster):
    assert cluster_with_host.info().HOSTS
    cant_be_deleted__test(one.cluster, cluster_with_host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_cluster_with_datastore(one: One, cluster_with_datastore: Cluster):
    assert cluster_with_datastore.info().DATASTORES
    cant_be_deleted__test(one.cluster, cluster_with_datastore)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_cluster_with_vnet(one: One, cluster_with_vnet: Cluster):
    assert cluster_with_vnet.info().VNETS
    cant_be_deleted__test(one.cluster, cluster_with_vnet)
