import pytest

from typing             import List
from api                import One
from utils.other        import get_unic_name
from config.opennebula  import VmStates, VmRecoverOperations





@pytest.fixture
def vms(one: One):
    vms_list = []

    for _ in range(5):
        vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n", False)
        vms_list.append(vm_id)

    yield vms_list

    for vm in vms_list:
        one.vm.recover(vm, VmRecoverOperations.DELETE)





# =================================================================================================
# TESTS
# =================================================================================================



def test_all_vms(one: One, vms: List[int]):
    created_vm_ids = vms

    filter_flag      = -2
    start_id         = -1
    end_id           = -1
    vm_state_filter  = -2   # all states (even DONE)
    key_value_filter = ""

    vmpool = one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM
    vmpool_ids = [vm.ID for vm in vmpool]
    
    assert set(created_vm_ids).issubset(vmpool_ids)



def test_state_filter(one: One, vms: List[int]):
    filter_flag      = -2
    start_id         = -1
    end_id           = -1
    vm_state_filter  = -1   # except DONE vms
    key_value_filter = ""

    vmpool = one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM


    for vm in vmpool:
        assert vm.STATE != VmStates.DONE



def test_start_id_filter(one: One, vms: List[int]):
    vm_ids = vms

    filter_flag      = -2
    start_id         = vm_ids[2]
    end_id           = -1
    vm_state_filter  = -2
    key_value_filter = ""

    vmpool = one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM

    for vm in vmpool:
        assert vm.ID >= start_id
    

def test_end_id_filter(one: One, vms: List[int]):
    vm_ids = vms

    filter_flag      = -2
    start_id         = -1
    end_id           = vm_ids[4]
    vm_state_filter  = -2   # all states
    key_value_filter = ""

    vmpool = one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM


    for vm in vmpool:
        assert vm.ID <= end_id


def test_vm_range(one: One, vms: List[int]):
    vm_ids = vms

    filter_flag      = -2
    start_id         = vm_ids[2]
    end_id           = vm_ids[4]
    vm_state_filter  = -2   # all states
    key_value_filter = ""

    vmpool = one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM

    for vm in vmpool:
        assert vm.ID >= start_id and vm.ID <= end_id





def test_user_template(one: One, dummy_vm: int):
    vm_id = dummy_vm

    filter_flag      = -2
    start_id         = vm_id
    end_id           = vm_id
    vm_state_filter  = -2   # all states
    key_value_filter = ""

    one.vm.update(vm_id, "TEST=test_value", 1)

    assert not one.vmpool.info(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM[0].USER_TEMPLATE
    assert one.vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter).VM[0].USER_TEMPLATE
    