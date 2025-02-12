import pytest
import time

from pyone              import OneException
from api                import One
from utils              import get_unic_name, kinit, run_command
from one_cli.image      import Image
from one_cli.vm         import VirtualMachine
from config             import ADMIN_NAME, ADMIN_PASSWORD, VmLcmStates, VmStates



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
        FORMAT = qcow2
    """
    image_id = one.image.allocate(template, 1)
    yield Image(image_id)
    one.image.delete(image_id)




@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm_with_disk(one: One, image: Image):
    template = f"""
        CPU    = 0.1
        MEMORY = 1
        DISK   = [IMAGE_ID = {image._id}]
    """

    vm_id = one.vm.allocate(template)
    time.sleep(3)

    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: time.sleep(0.1)

    yield VirtualMachine(vm_id)

    run_command(f"sudo -u brestadm onevm terminate --hard {vm_id}")

    while one.vm.info(vm_id).STATE != VmStates.DONE: time.sleep(0.1)



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.snapshotcreate(999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_create_snapshot(one: One, vm_with_disk: VirtualMachine):
    vm_id            = vm_with_disk._id
    snapshot_name    = get_unic_name()
    
    next_snapshot_id = 0
    snapshots_count  = 0


    kinit(ADMIN_NAME, ADMIN_PASSWORD, "bufn1")
    run_command(f"sudo -u brestadm onevm resume {vm_id}")
    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: time.sleep(0.1)


    _id = one.vm.snapshotcreate(vm_id, snapshot_name)
    assert one.vm.info(vm_id).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT

    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: time.sleep(0.1)

    assert _id == next_snapshot_id
    next_snapshot_id += 1
    snapshots_count  += 1

    snapshots = one.vm.info(vm_id).TEMPLATE.get("SNAPSHOT", [])
    assert len(snapshots) == snapshots_count
    assert snapshots[0]["NAME"] == snapshot_name

    _id = one.vm.snapshotcreate(vm_id, "")
    time.sleep(5)

    assert _id == next_snapshot_id
    next_snapshot_id += 1
    snapshots_count  += 1

    assert len(one.vm.info(vm_id).TEMPLATE.get("SNAPSHOT", [])) == snapshots_count



