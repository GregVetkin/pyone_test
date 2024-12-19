import pytest

from random             import randint
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from config             import ADMIN_NAME




@pytest.fixture(scope="module")
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



@pytest.fixture(scope="module")
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()


@pytest.fixture(scope="module")
def vm_with_disk(image: Image):
    vm_id = create_vm(f"CPU=1\nMEMORY=1\nDISK=[IMAGE_ID={image._id}]", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.disk_detach(0)
    wait_vm_offline(vm_id)
    vm.terminate()
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.diskresize(999999, 0, "100")



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disk_not_exist(one: One, vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.diskresize(vm._id, 999999, "100")



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_resize_vm_disk(one: One, vm_with_disk: VirtualMachine):
    current_disk_size  = int(one.vm.info(vm_with_disk._id).TEMPLATE["DISK"]["SIZE"])
    planned_disk_size  = current_disk_size + randint(1, 30)

    _id = one.vm.diskresize(vm_with_disk._id, 0, f"{planned_disk_size}")
    wait_vm_offline(vm_with_disk._id)
    assert _id == vm_with_disk._id
    assert int(one.vm.info(vm_with_disk._id).TEMPLATE["DISK"]["SIZE"]) == planned_disk_size



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_reduce_vm_disk_size(one: One, vm_with_disk: VirtualMachine):
    current_disk_size  = int(one.vm.info(vm_with_disk._id).TEMPLATE["DISK"]["SIZE"])
    planned_disk_size  = current_disk_size - 1

    with pytest.raises(OneException):
        one.vm.diskresize(vm_with_disk._id, 0, f"{planned_disk_size}")

    assert int(one.vm.info(vm_with_disk._id).TEMPLATE["DISK"]["SIZE"]) == current_disk_size


