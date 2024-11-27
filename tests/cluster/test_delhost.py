import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster, cluster_exist
from one_cli.host       import Host, create_host
from config             import ADMIN_NAME




@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(hostname=get_unic_name())
    host    = Host(host_id)
    yield host
    host.delete()



@pytest.fixture
def cluster():
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    yield cluster
    cluster.delete()




@pytest.fixture
def cluster_with_host(host):
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    cluster.addhost(host._id)
    yield cluster
    cluster.delhost(host._id)
    cluster.delete()




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One, host: Host):
    with pytest.raises(OneException):
        one.cluster.delhost(999999, host._id)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One, cluster: Cluster):
    with pytest.raises(OneException):
        one.cluster.delhost(cluster._id, 999999)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_remove_datastore_from_cluster(one: One, cluster_with_host: Cluster):
    old_cluster_hosts = cluster_with_host.info().HOSTS
    assert old_cluster_hosts
    host_id = old_cluster_hosts[0]

    _id = one.cluster.delhost(cluster_with_host._id, host_id)
    assert _id == cluster_with_host._id

    new_cluster_hosts = cluster_with_host.info().HOSTS
    assert host_id not in new_cluster_hosts
    assert len(new_cluster_hosts) == len(old_cluster_hosts) - 1
