import pytest

from time               import sleep
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image
from one_cli.vm         import VirtualMachine
from config             import ADMIN_NAME



def await_vm_status_code(one: One, vm_id: int, status_code: int, intervals=1.0):
    while one.vm.info(vm_id).STATE != status_code:
        sleep(intervals)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    ds_id = 1
    for ds in one.datastorepool.info().DATASTORE:
        if ds.NAME.startswith("image_"):
            ds_id = ds.ID
            break

    _id = one.image.allocate(template, ds_id, False)

    yield Image(_id)

    while one.image.info(_id).STATE != 1:
        sleep(1)

    one.image.delete(_id, True)



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n")
    await_vm_status_code(one, vm_id, 8)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)
    await_vm_status_code(one, vm_id, 6)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm_with_disk(one: One, image: Image, vm: VirtualMachine): 
    one.vm.attach(vm._id, f"DISK=[IMAGE_ID={image._id}]")
    await_vm_status_code(one, vm._id, 8)

    yield VirtualMachine(vm._id)

    one.vm.detach(vm._id, 0)
    await_vm_status_code(one, vm._id, 8)
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    vm_id       = 9999999
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disk_not_exist(one: One, vm: VirtualMachine):
    vm_id       = vm._id
    disk_id     = 999999
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_snapshot_not_exist(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = 99999

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_type_not_exist(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = "NONE"
    snapshot_id = -1

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_name_is_taken(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    image_id    = int(one.vm.info(vm_id).TEMPLATE["DISK"]["IMAGE_ID"])
    image_name  = one.image.info(image_id).NAME
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_name(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    image_name  = ""
    image_type  = ""
    snapshot_id = -1

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disksaveas__cold(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    image_name  = get_unic_name()
    image_type  = ""
    snapshot_id = -1

    assert one.vm.info(vm_with_disk._id).STATE == 8
    _id  = one.vm.disksaveas(vm_id, disk_id, image_name, image_type, snapshot_id)
    assert one.image.info(_id).NAME == image_name

    one.image.delete(_id)

