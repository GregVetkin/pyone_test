import pytest
import random
import pyone

from api                import One

from utils.kerberos     import PyoneWrap
from utils.other        import wait_until

from config.base        import API_URI, BrestAdmin
from config.opennebula  import VmStates



@pytest.fixture
def dummy_vm_poweroff(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    return vm_id




# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id   = random.randint(9999, 999999)
    disk_id = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.detach(vm_id, disk_id)



def test_disk_not_exist(one: One, dummy_vm_poweroff: int):
    vm_id   = dummy_vm_poweroff
    disk_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.vm.detach(vm_id, disk_id)



def test_detach(one: One, poweroff_vm_mini: int):
    vm_id    = poweroff_vm_mini
    vm_info  = one.vm.info(vm_id, False)
    vm_disks = vm_info.TEMPLATE["DISK"]

    if isinstance(vm_disks, dict):
        disk_count_before = 1
        disk_id = int(vm_disks["DISK_ID"])

    elif isinstance(vm_disks, list):
        disk_count_before = len(vm_disks)
        disk_id = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    else:
        raise "ВМ без дисков"
    
    
    _id = one.vm.detach(vm_id, disk_id)
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, False)
    vm_template = vm_info.TEMPLATE

    if "DISK" not in vm_template:
        disk_count_after = 0

    elif isinstance(vm_template["DISK"], dict):
        disk_count_after = 1
        
    else:
        disk_count_after = len(vm_template["DISK"])

    assert disk_count_after - disk_count_before == -1

    if disk_count_after > 1:
        assert disk_id not in [int(disk["DISK_ID"] for disk in vm_template["DISK"])]
    
    if disk_count_after == 1:
        assert disk_id != int(vm_template["DISK"]["DISK_ID"])



@pytest.mark.KERBEROS
def test_detach_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id   = poweroff_vm_mini
    vm_info = one.vm.info(vm_id, False)
    vm_disks = vm_info.TEMPLATE["DISK"]

    if isinstance(vm_disks, dict):
        disk_count_before = 1
        disk_id = int(vm_disks["DISK_ID"])

    elif isinstance(vm_disks, list):
        disk_count_before = len(vm_disks)
        disk_id = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    else:
        raise "ВМ без дисков"
    
    
    _id = one.vm.detach(vm_id, disk_id, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, False)
    vm_template = vm_info.TEMPLATE

    if "DISK" not in vm_template:
        disk_count_after = 0

    elif isinstance(vm_template["DISK"], dict):
        disk_count_after = 1

    else:
        disk_count_after = len(vm_template["DISK"])

    assert disk_count_after - disk_count_before == -1

    if disk_count_after > 1:
        assert disk_id not in [int(disk["DISK_ID"] for disk in vm_template["DISK"])]
    
    if disk_count_after == 1:
        assert disk_id != int(vm_template["DISK"]["DISK_ID"])
