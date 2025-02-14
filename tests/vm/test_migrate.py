import pytest
import random
from pyone           import OneException, OneNoExistsException
from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME, VmStates, VmLcmStates



@pytest.fixture()
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
    vm_id   = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=999\nMEMORY=999999\n", True)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    one.vm.deploy(vm_id, host_id, False)
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



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_certain_host(one: One, vm: VirtualMachine):
    vm_id           = vm._id
    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    _id = one.vm.migrate(vm_id, target_host_id)
    assert _id == vm_id
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID == target_host_id



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_certain_datastore(one: One, vm: VirtualMachine):
    vm_id               = vm._id
    current_host_id     = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id       = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID
    current_ds_tm_mad   = one.datastore.info(current_ds_id).TM_MAD
    target_host_id      = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    target_ds_id        = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE if ds.TYPE == 1 and ds.TM_MAD == current_ds_tm_mad and ds.ID != current_ds_id])

    _id = one.vm.migrate(vm_id, target_host_id, datastore_id=target_ds_id)
    assert _id == vm_id
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID   == target_host_id
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID == target_ds_id



@pytest.mark.parametrize("ds_type", [0, 2])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_wrong_datastore_type(one: One, vm: VirtualMachine, ds_type: int):
    vm_id           = vm._id
    current_host_id = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id   = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    target_ds_id    = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE if ds.TYPE == ds_type])

    with pytest.raises(OneException):
        one.vm.migrate(vm_id, target_host_id, datastore_id=target_ds_id)

    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID   == current_host_id
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID == current_ds_id



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_different_datastore_tm_driver(one: One, vm: VirtualMachine):
    vm_id               = vm._id
    current_host_id     = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id       = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID
    current_ds_tm_mad   = one.datastore.info(current_ds_id).TM_MAD
    target_host_id      = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    target_ds_id        = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE if ds.TYPE == 1 and ds.TM_MAD != current_ds_tm_mad])

    with pytest.raises(OneException):
        one.vm.migrate(vm_id, target_host_id, datastore_id=target_ds_id)

    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID   == current_host_id
    assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].DS_ID == current_ds_id



@pytest.mark.parametrize("check_capacity", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_capacity_check(one: One, large_vm: VirtualMachine, check_capacity: bool):
    vm_id           = large_vm._id
    current_host_id = one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID
    target_host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    if check_capacity:
        with pytest.raises(OneException):
            one.vm.migrate(vm_id, target_host_id, host_capacity_check=check_capacity)
        assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID == current_host_id
    else:
        _id = one.vm.migrate(vm_id, target_host_id, host_capacity_check=check_capacity)
        assert _id == vm_id
        assert one.vm.info(vm_id).HISTORY_RECORDS.HISTORY[-1].HID == target_host_id


