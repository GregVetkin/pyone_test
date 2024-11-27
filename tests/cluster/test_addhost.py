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
        one.cluster.addhost(999999, host._id)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One, cluster: Cluster):
    with pytest.raises(OneException):
        one.cluster.addhost(cluster._id, 999999)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_add_host_to_cluster(one: One, cluster: Cluster, host: Host):
    assert host._id not in cluster.info().HOSTS
    one.cluster.addhost(cluster._id, host._id)
    assert host._id in cluster.info().HOSTS


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_add_added_host_to_cluster(one: One, cluster_with_host: Cluster):
    old_cluster_hosts = cluster_with_host.info().HOSTS
    assert old_cluster_hosts
    added_host_id = old_cluster_hosts[0]
    one.cluster.addhost(cluster_with_host._id, added_host_id)
    new_cluster_hosts = cluster_with_host.info().HOSTS
    assert added_host_id in new_cluster_hosts
    assert len(old_cluster_hosts) == len(new_cluster_hosts)
