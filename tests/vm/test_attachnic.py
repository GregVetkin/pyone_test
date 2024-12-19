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


@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One, vnet: Vnet):
    with pytest.raises(OneException):
        one.vm.attachnic(999999, f"NIC=[NETWORK_ID={vnet._id}]")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vnet_not_exist(one: One, vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.attachnic(vm._id, "NIC=[NETWORK_ID=99999]")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_attach_nic_to_vm(one: One, vm: VirtualMachine, vnet: Vnet):
    _id = one.vm.attachnic(vm._id, f"NIC=[NETWORK_ID={vnet._id}]")
    assert _id == vm._id
    wait_vm_offline(vm._id)
    
    assert int(one.vm.info(vm._id).TEMPLATE["NIC"]["NETWORK_ID"]) == vnet._id
    vm.nic_detach(0)
    wait_vm_offline(vm._id)

