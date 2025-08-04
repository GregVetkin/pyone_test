import pytest
import pyone
import random
from api            import One
from utils.other    import get_unic_name




def test_cluster_not_exist(one: One):
    host_name = get_unic_name()
    im_mad = "kvm"
    vm_mad = "kvm"
    cluster_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        one.host.allocate(host_name, im_mad, vm_mad, cluster_id)



def test_allocate_with_default_cluster(one: One):
    host_name = get_unic_name()
    im_mad = "kvm"
    vm_mad = "kvm"
    cluster_id = -1

    host_id = one.host.allocate(host_name, im_mad, vm_mad, cluster_id)
    assert one.host.info(host_id, False).NAME == host_name
    one.host.delete(host_id)



def test_allocate_with_specific_cluster(one: One, dummy_cluster):
    host_name  = get_unic_name()
    im_mad = "kvm"
    vm_mad = "kvm"
    cluster_id = dummy_cluster

    host_id = one.host.allocate(host_name, im_mad, vm_mad, cluster_id)
    assert cluster_id == one.host.info(host_id, False).CLUSTER_ID
    one.host.delete(host_id)


