import pytest
import random
from pyone           import OneException, OneNoExistsException
from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME, VmStates



@pytest.fixture(scope="module")
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", False)
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.recover(vm_id, 3)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def large_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", False)
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.recover(vm_id, 3)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exists(one: One):
    target_host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
   
    with pytest.raises(OneNoExistsException):
        one.vm.migrate(vm_id=99999, host_id=target_host_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exists(one: One, vm: VirtualMachine):
    with pytest.raises(OneNoExistsException):
        one.vm.migrate(vm_id=vm._id, host_id=99999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exists(one: One, vm: VirtualMachine):
    vm_id           = vm._id
    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    
    with pytest.raises(OneNoExistsException):
        one.vm.migrate(vm_id, target_host_id, datastore_id=99999)



@pytest.mark.parametrize("check_capacity", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_check_host_capacity(one: One, large_vm: VirtualMachine, check_capacity: bool):
    vm_id           = large_vm._id
    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    if check_capacity:
        with pytest.raises(OneException):
            one.vm.migrate(vm_id, target_host_id, host_capacity_check=check_capacity)
    else:
        _id = one.vm.migrate(vm_id, target_host_id, host_capacity_check=check_capacity)
        assert _id == vm_id



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_certain_host(one: One, vm: VirtualMachine):
    vm_id           = vm._id
    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    _id = one.vm.migrate(vm_id, target_host_id)
    assert _id == vm_id
    assert one.vm.info(21).HISTORY_RECORDS.HISTORY[-1].HID == target_host_id


