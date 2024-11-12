import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.host       import Host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)





# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_cluster_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.allocate(hostname="GregVetkin", im_mad="kvm", vm_mad="kvm", cluster_id=999999)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_bad_IM_MAD(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.allocate(hostname="GregVetkin", im_mad="notexist", vm_mad="kvm", cluster_id=-1)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_bad_VM_MAD(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.allocate(hostname="GregVetkin", im_mad="kvm", vm_mad="notexist", cluster_id=-1)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_allocate_host_kvm_kvm(one: One):
    host_id = one.host.allocate(hostname="GregVetkin", im_mad="kvm", vm_mad="kvm", cluster_id=-1)
    host    = Host(host_id)
    assert host_exist(host_id)
    host.delete()

