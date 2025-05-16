import pytest
import random
from pyone           import OneException
from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME, VmStates




@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def undeployed_vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n")
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    one.vm.action("undeploy-hard", vm_id)
    while one.vm.info(vm_id).STATE != VmStates.UNDEPLOYED: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def large_hold_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=99999\nMEMORY=1\n", True)
    while one.vm.info(vm_id).STATE != VmStates.HOLD: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.recover(vm_id, 3)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def hold_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", True)
    while one.vm.info(vm_id).STATE != VmStates.HOLD: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.recover(vm_id, 3)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.deploy(99999, 0)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One, hold_vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.deploy(hold_vm._id, 999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_deploy_on_host(one: One, undeployed_vm: VirtualMachine):
    vm_id           = undeployed_vm._id
    host_ids_list   = [host.ID for host in one.hostpool.info().HOST]
    target_host_id  = random.choice(host_ids_list)

    _id = one.vm.deploy(vm_id, target_host_id)
    assert _id == vm_id
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)
    assert vm_id in one.host.info(target_host_id).VMS.ID


@pytest.mark.parametrize("check_capacity", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_check_host_capacity(one: One, large_hold_vm: VirtualMachine, check_capacity: bool):
    vm_id           = large_hold_vm._id
    host_ids_list   = [host.ID for host in one.hostpool.info().HOST]
    target_host_id  = random.choice(host_ids_list)

    if check_capacity:
        with pytest.raises(OneException):
            one.vm.deploy(vm_id, target_host_id, check_capacity)
    else:
        _id = one.vm.deploy(vm_id, target_host_id, check_capacity)
        assert _id == vm_id 



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_certain_datastore(one: One, hold_vm: VirtualMachine):
    vm_id           = hold_vm._id
    host_ids        = [host.ID for host in one.hostpool.info().HOST]
    system_ds_ids   = [datastore.ID for datastore in one.datastorepool.info().DATASTORE if datastore.TYPE == 1]
    target_host_id  = random.choice(host_ids)
    target_ds_id    = random.choice(system_ds_ids)

    _id = one.vm.deploy(vm_id, target_host_id, datastore_id=target_ds_id)
    assert _id == vm_id
    # sleep(5)
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID == target_ds_id


