import pytest
import pyone
from api            import One
from utils.other    import get_unic_name





def test_specified_cluster_does_not_exist(one: One):
    with pytest.raises(pyone.OneNoExistsException):
        one.host.allocate(hostname=get_unic_name(), im_mad="kvm", vm_mad="kvm", cluster_id=999999)


def test_allocate_host_kvm_kvm(one: One):
    host_name = get_unic_name()
    host_id   = one.host.allocate(host_name, "kvm", "kvm", -1)
    assert one.host.info(host_id).NAME == host_name
    one.host.delete(host_id)


def test_specific_cluster(one: One, dummy_cluster):
    host_name  = get_unic_name()
    cluster_id = dummy_cluster
    host_id    = one.host.allocate(host_name, "kvm", "kvm", cluster_id)
    host_info  = one.host.info(host_id)
    assert cluster_id == host_info.CLUSTER_ID
    one.host.delete(host_id)


