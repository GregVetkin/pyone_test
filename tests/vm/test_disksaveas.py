import pyone.acl
import pytest
import pyone
import random

from api                import One

from utils.other        import get_unic_name
from utils.kerberos     import PyoneWrap

from config.base        import API_URI, BrestAdmin



IMAGE_TYPES = {0: "OS",
               1: "CDROM",
               2: "DATABLOCK"}


# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id       = random.randint(9999, 999999)
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)


def test_disk_not_exist(one: One, dummy_vm: int):
    vm_id       = dummy_vm
    disk_id     = random.randint(9999, 999999)
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(pyone.OneInternalException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)


def test_snapshot_not_exist(one: One, poweroff_vm_mini: int):
    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneInternalException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)


def test_type_not_exist(one: One, poweroff_vm_mini: int):
    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = "NONE"
    snapshot_id = -1

    with pytest.raises(pyone.OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)


def test_name_is_taken(one: One, poweroff_vm_mini: int, dummy_image: int):
    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = one.image.info(dummy_image, False).NAME
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(pyone.OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)


def test_empty_name(one: One, poweroff_vm_mini: int):
    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = ""
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(pyone.OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)






def test_disksaveas(one: One, poweroff_vm_mini: int):
    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = random.choice(list(IMAGE_TYPES.values()))
    snapshot_id = -1


    _id  = one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)

    image_info = one.image.info(_id, False)
    assert image_info.NAME == image_name
    assert IMAGE_TYPES[image_info.TYPE] == image_type

    one.image.delete(_id, True)


@pytest.mark.KERBEROS
def test_disksaveas_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id       = poweroff_vm_mini
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = random.choice(list(IMAGE_TYPES.values()))
    snapshot_id = -1


    _id  = one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id, pw.sessionDir)
    pw.run_one_vm_action()

    image_info = one.image.info(_id, False)
    assert image_info.NAME == image_name
    assert IMAGE_TYPES[image_info.TYPE] == image_type

    one.image.delete(_id, True)