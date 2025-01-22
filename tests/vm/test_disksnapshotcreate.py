import pytest

from time               import sleep
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image, image_exist
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline, vm_exist
from config             import ADMIN_NAME



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

    image_id = create_image(ds_id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture()
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
        one.vm.disksnapshotcreate(99999, 0, "Test")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disk_not_exist(one: One, vm_with_disk: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.disksnapshotcreate(vm_with_disk._id, 999999, "Test")
    

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_create_disk_snapshot(one: One, vm_with_disk: VirtualMachine):
    assert not one.vm.info(vm_with_disk._id).SNAPSHOTS

    snapshot_name = get_unic_name()
    snapshot_id   = one.vm.disksnapshotcreate(vm_with_disk._id, 0, snapshot_name)
    sleep(1)
    snapshots     = one.vm.info(vm_with_disk._id).SNAPSHOTS
    
    assert snapshots[0].SNAPSHOT[0]
    assert snapshots[0].SNAPSHOT[0].ACTIVE  == "YES"
    assert snapshots[0].SNAPSHOT[0].ID      == snapshot_id
    assert snapshots[0].SNAPSHOT[0].NAME    == snapshot_name

    