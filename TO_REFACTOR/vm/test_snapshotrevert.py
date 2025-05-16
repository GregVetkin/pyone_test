import pytest
import time
import random
from pyone              import OneException
from api                import One
from utils              import get_unic_name, kinit, run_command
from one_cli.image      import Image, create_image
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from config             import ADMIN_NAME, ADMIN_PASSWORD, VmLcmStates, VmStates



@pytest.fixture()
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1\nVCPU=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()


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
def vm_with_snapshots(one: One, image: Image):
    template = f"""
        CPU    = 0.1
        MEMORY = 1
        DISK   = [IMAGE_ID = {image._id}]
    """

    vm_id = one.vm.allocate(template)
    time.sleep(3)

    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: time.sleep(0.1)
    
    kinit(ADMIN_NAME, ADMIN_PASSWORD, "bufn1")
    run_command(f"sudo -u brestadm onevm resume {vm_id}")
    time.sleep(5)

    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: time.sleep(0.1)

    for _ in range(random.randrange(2, 5)):
        one.vm.snapshotcreate(vm_id)
        time.sleep(1)

    time.sleep(5)

    yield VirtualMachine(vm_id)

    run_command(f"sudo -u brestadm onevm terminate --hard {vm_id}")
    while one.vm.info(vm_id).STATE != VmStates.DONE: time.sleep(0.1)


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.snapshotrevert(999999, 0)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_snapshot_not_exist(one: One, vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.snapshotrevert(vm._id, 999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_revert_snapshot(one: One, vm_with_snapshots: VirtualMachine):
    vm_id        = vm_with_snapshots._id
    snapshot_ids = [int(snapshot_info["SNAPSHOT_ID"]) for snapshot_info in one.vm.info(vm_id).TEMPLATE.get("SNAPSHOT", [])]
    target_snapshot_id = random.choice(snapshot_ids)

    if one.vm.info(vm_id).STATE == VmStates.POWEROFF:
        kinit(ADMIN_NAME, ADMIN_PASSWORD, "bufn1")
        run_command(f"sudo -u brestadm onevm resume {vm_id}")
        while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: time.sleep(0.1)

    _id = one.vm.snapshotrevert(vm_id, target_snapshot_id)
    assert one.vm.info(vm_id).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT
    assert _id == vm_id
    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: time.sleep(0.1)

    assert not one.vm.info(vm_id).USER_TEMPLATE.get("ERROR")

