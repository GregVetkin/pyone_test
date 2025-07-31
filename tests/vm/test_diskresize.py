import pytest
import pyone
import random

from api                import One

from utils.other        import wait_until
from utils.kerberos     import PyoneWrap

from config.opennebula  import VmLcmStates, VmStates
from config.base        import API_URI, BrestAdmin




def test_vm_not_exist(one: One):
    vm_id    = random.randint(9999, 999999)
    disk_id  = 0
    new_size = "4096"

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.diskresize(vm_id, disk_id, new_size)




def test_disk_not_exist(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    disk_id  = random.randint(9999, 999999)
    new_size = "4096"

    with pytest.raises(pyone.OneActionException):
        one.vm.diskresize(vm_id, disk_id, new_size)




def test_cant_reduce_disk_size(one: One, poweroff_vm_mini: int):
    vm_id   = poweroff_vm_mini
    disk_id = 0

    disk_size_before  = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])    # если дисков несколько - будет список со словарями
    planned_disk_size = disk_size_before // random.randint(2, disk_size_before)

    with pytest.raises(pyone.OneActionException):
        one.vm.diskresize(vm_id, disk_id, f"{planned_disk_size}")

    disk_size_after = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])
    assert disk_size_after == disk_size_before




def test_resize_vm_disk(one: One, poweroff_vm_mini: int):
    vm_id   = poweroff_vm_mini
    disk_id = 0

    disk_size_before  = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])
    planned_disk_size = disk_size_before + random.randint(512, 2048)

    _id = one.vm.diskresize(vm_id, disk_id, f"{planned_disk_size}")

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.DISK_RESIZE_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE != VmLcmStates.DISK_RESIZE_POWEROFF)

    disk_size_after = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])
    assert disk_size_after == planned_disk_size

    assert _id == vm_id, "сейчас возвращает disk_id, но по документации должен vm_id"




@pytest.mark.KERBEROS
def test_resize_vm_disk_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id   = poweroff_vm_mini
    disk_id = 0

    disk_size_before  = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])
    planned_disk_size = disk_size_before + random.randint(512, 2048)

    _id = one.vm.diskresize(vm_id, disk_id, f"{planned_disk_size}", pw.sessionDir)
    pw.run_one_vm_action()
    
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.DISK_RESIZE_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE != VmLcmStates.DISK_RESIZE_POWEROFF)

    disk_size_after = int(one.vm.info(vm_id, False).TEMPLATE["DISK"]["SIZE"])
    assert disk_size_after == planned_disk_size

    assert _id == vm_id, "сейчас возвращает disk_id, но по документации должен vm_id"
