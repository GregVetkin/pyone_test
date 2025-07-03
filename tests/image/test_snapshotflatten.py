import pytest
import random

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils.other        import wait_until
from config.opennebula  import VmStates, ImageStates



@pytest.fixture
def image_with_snapshots(one: One, dummy_image: int, dummy_vm: int):
    wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    one.image.persistent(dummy_image, True)
    wait_until(lambda: one.image.info(dummy_image).PERSISTENT == 1)

    one.vm.attach(dummy_vm, f"DISK=[IMAGE_ID={dummy_image}]")
    wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    for _ in range(5):
        one.vm.disksnapshotcreate(dummy_vm, 0, "")
        wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    one.vm.recover(dummy_vm, 3) # delete vm

    yield dummy_image

    wait_until(lambda: one.image.info(dummy_image).STATE == ImageStates.READY)




# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist(one: One):
    image_id = 99999
    snap_id  = 0

    with pytest.raises(OneNoExistsException):
        one.image.snapshotflatten(image_id, snap_id)



def test_snapshot_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    snap_id  = 99999

    with pytest.raises(OneActionException):
        one.image.snapshotflatten(image_id, snap_id)



def test_not_active_snapshot(one: One, image_with_snapshots: int):
    image_id        = image_with_snapshots
    image_snapshots = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    assert len(image_snapshots) > 1


    not_active_snap_ids = [snapshot.ID for snapshot in image_snapshots if not snapshot.ACTIVE]
    snap_id             = random.choice(not_active_snap_ids)

    _id = one.image.snapshotflatten(image_id, snap_id)
    assert _id == snap_id

    wait_until(lambda: one.image.info(image_id).STATE == ImageStates.READY)
    assert not one.image.info(image_id).SNAPSHOTS.SNAPSHOT



def test_active_snapshot(one: One, image_with_snapshots: int):
    image_id        = image_with_snapshots
    image_snapshots = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    assert len(image_snapshots) > 1

    active_snap_id  = next(snapshot.ID for snapshot in image_snapshots if snapshot.ACTIVE)

    _id = one.image.snapshotflatten(image_id, active_snap_id)
    assert _id == active_snap_id

    wait_until(lambda: one.image.info(image_id).STATE == ImageStates.READY)
    assert not one.image.info(image_id).SNAPSHOTS.SNAPSHOT
