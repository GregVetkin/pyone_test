import pytest

from api                import One
from pyone              import OneNoExistsException, OneInternalException
from utils              import get_user_auth, get_unic_name
from one_cli.cluster    import Cluster, create_cluster
from one_cli.host       import Host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def cluster():
    _id = create_cluster(get_unic_name())
    cluster = Cluster(_id)
    yield cluster
    cluster.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_cluster_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.allocate(hostname=f"{get_unic_name()}", im_mad="kvm", vm_mad="kvm", cluster_id=999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_allocate_host_kvm_kvm(one: One):
    _id  = one.host.allocate(hostname=f"{get_unic_name()}", im_mad="kvm", vm_mad="kvm", cluster_id=-1)
    assert host_exist(_id)
    Host(_id).delete()



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_create_host_with_certain_cluster(one: One, cluster: Cluster):
    _id  = one.host.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs", cluster_id=cluster._id)
    host = Host(_id)
    assert host_exist(_id)
    assert cluster._id == host.info().CLUSTER_ID
    host.delete()


