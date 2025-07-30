import pytest
import random
import pyone

from api                import One
from utils.other        import wait_until
from config.opennebula  import VmStates, ImageStates, VmRecoverOperations



@pytest.fixture
def image_with_snapshots(one: One, dummy_image: int, dummy_vm: int):
    image_id = dummy_image
    vm_id = dummy_vm

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    one.image.persistent(image_id, True)
    wait_until(lambda: one.image.info(image_id, False).PERSISTENT == 1)

    one.vm.attach(vm_id, f"DISK=[IMAGE_ID={image_id}]")
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    for _ in range(3):
        one.vm.disksnapshotcreate(vm_id, 0, "")
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)

    yield image_id

    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)




# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist(one: One):
    image_id = random.randint(9999, 999999)
    snap_id  = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.image.snapshotflatten(image_id, snap_id)



def test_snapshot_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    snap_id  = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.image.snapshotflatten(image_id, snap_id)



def test_not_active_snapshot(one: One, image_with_snapshots: int):
    image_id        = image_with_snapshots
    image_snapshots = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    assert len(image_snapshots) > 1


    not_active_snap_ids = [snapshot.ID for snapshot in image_snapshots if not snapshot.ACTIVE]
    snap_id             = random.choice(not_active_snap_ids)

    _id = one.image.snapshotflatten(image_id, snap_id)
    assert _id == snap_id

    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)
    assert not one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT



def test_active_snapshot(one: One, image_with_snapshots: int):
    image_id        = image_with_snapshots
    image_snapshots = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    assert len(image_snapshots) > 1

    active_snap_id  = next(snapshot.ID for snapshot in image_snapshots if snapshot.ACTIVE)

    _id = one.image.snapshotflatten(image_id, active_snap_id)
    assert _id == active_snap_id

    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)
    assert not one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
