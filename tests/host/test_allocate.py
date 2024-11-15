import pytest

from api                import One
from pyone              import OneNoExistsException, OneInternalException
from utils              import get_user_auth, get_unic_name
from one_cli.host       import Host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)





# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_cluster_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.allocate(hostname=f"{get_unic_name()}", im_mad="kvm", vm_mad="kvm", cluster_id=999999)





@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_allocate_host_kvm_kvm(one: One):
    _id = one.host.allocate(hostname=f"{get_unic_name()}", im_mad="kvm", vm_mad="kvm", cluster_id=-1)
    assert host_exist(_id)
    Host(_id).delete()


