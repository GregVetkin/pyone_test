import pytest

from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.vnet       import Vnet, create_vnet
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from config             import ADMIN_NAME


@pytest.fixture(scope="module")
def vnet():
    vnet_template = f"""
        NAME   = {get_unic_name()}
        VN_MAD = bridge
        AR = [ 
            TYPE = IP4,
            IP   = 1.1.1.1,
            SIZE = 1
        ]
    """
    vnet_id = create_vnet(vnet_template)
    vnet    = Vnet(vnet_id)
    yield vnet
    vnet.delete()


# @pytest.fixture(scope="module")
# def vm():
#     vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
#     vm    = VirtualMachine(vm_id)
#     yield vm
#     vm.terminate()


@pytest.fixture(scope="module")
def vm_with_nic(vnet: Vnet):
    vm_id = create_vm(f"CPU=1\nMEMORY=1\nNIC=[NETWORK_ID={vnet._id}]", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.detachnic(999999, 0)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vnet_not_exist(one: One, vm_with_nic: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.detachnic(vm_with_nic._id, 99999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_attach_nic_to_vm(one: One, vm_with_nic: VirtualMachine):
    assert "NIC" in one.vm.info(vm_with_nic._id).TEMPLATE
    _id = one.vm.detachnic(vm_with_nic._id, 0)
    assert _id == vm_with_nic._id
    wait_vm_offline(vm_with_nic._id)
    assert "NIC" not in one.vm.info(vm_with_nic._id).TEMPLATE
