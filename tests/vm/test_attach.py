import pytest

from pyone              import OneException, OneNoExistsException
from api                import One
from utils.other        import wait_until
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmStates, VmLcmStates
from config.base        import API_URI, BrestAdmin, BREST_VERSION



@pytest.fixture
def dummy_vm_poweroff(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    return vm_id



# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One, dummy_image: int):
    vm_id    = 99999
    image_id = dummy_image
    template = f"DISK=[IMAGE_ID={image_id}]"

    with pytest.raises(OneNoExistsException):
        one.vm.attach(vm_id, template)



def test_image_not_exist(one: One, dummy_vm_poweroff: int):
    vm_id    = dummy_vm_poweroff
    image_id = 99999
    template = f"DISK=[IMAGE_ID={image_id}]"

    with pytest.raises(OneException):
        one.vm.attach(vm_id, template)



def test_attach_disk(one: One, dummy_vm_poweroff: int, dummy_image: int):
    vm_id    = dummy_vm_poweroff
    image_id = dummy_image
    template = f"DISK=[IMAGE_ID={image_id}]"

    vm_template_before = one.vm.info(vm_id, True).TEMPLATE

    if "DISK" not in vm_template_before:
        disk_count_brefore = 0
    elif isinstance(vm_template_before["DISK"], dict):
        disk_count_brefore = 1
    else:
        disk_count_brefore = len(vm_template_before["DISK"])


    _id = one.vm.attach(vm_id, template)
    assert _id == vm_id
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)


    vm_template = one.vm.info(vm_id, True).TEMPLATE
    vm_disks = vm_template["DISK"]


    if isinstance(vm_disks, dict):
        disk_count_after = 1
        vm_disk = vm_disks
    else:
        disk_count_after = len(vm_disks)
        vm_disk = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    assert disk_count_after - disk_count_brefore == 1
    assert int(vm_disk["IMAGE_ID"]) == image_id

    one.vm.detach(vm_id, int(vm_disk["DISK_ID"]))
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)


@pytest.mark.KERBEROS
def test_attach_KERBEROS(dummy_vm_poweroff: int, dummy_image: int):
    pw    = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one   = pw.get_client()


    vm_id    = dummy_vm_poweroff
    image_id = dummy_image
    template = f"DISK=[IMAGE_ID={image_id}]"

    vm_template_before = one.vm.info(vm_id, True).TEMPLATE

    if "DISK" not in vm_template_before:
        disk_count_brefore = 0
    elif isinstance(vm_template_before["DISK"], dict):
        disk_count_brefore = 1
    else:
        disk_count_brefore = len(vm_template_before["DISK"])


    _id = one.vm.attach(vm_id, template, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id
    wait_until(lambda: one.vm.info(vm_id, True).STATE == VmStates.POWEROFF)


    vm_template = one.vm.info(vm_id, True).TEMPLATE
    vm_disks = vm_template["DISK"]


    if isinstance(vm_disks, dict):
        disk_count_after = 1
        vm_disk = vm_disks
    else:
        disk_count_after = len(vm_disks)
        vm_disk = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    assert disk_count_after - disk_count_brefore == 1
    assert int(vm_disk["IMAGE_ID"]) == image_id

    one.vm.detach(vm_id, int(vm_disk["DISK_ID"]))
    wait_until(lambda: one.vm.info(vm_id, True).STATE == VmStates.POWEROFF)

