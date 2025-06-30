import pytest
import time

from config.opennebula  import VmStates, ImageStates
from api                import One
from pyone              import OneNoExistsException, OneActionException, OneException
from utils.other        import wait_until




@pytest.fixture
def image_with_snapshots(one: One, dummy_image: int, dummy_vm: int):
    wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    one.image.persistent(dummy_image, True)
    wait_until(lambda: one.image.info(dummy_image).PERSISTENT == 1)

    one.vm.attach(dummy_vm, f"DISK=[IMAGE_ID={dummy_image}]")
    wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    for _ in range(3):
        one.vm.disksnapshotcreate(dummy_vm, 0, "")
        wait_until(lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF)

    one.vm.recover(dummy_vm, 3) # delete vm

    yield dummy_image

    wait_until(lambda: one.image.info(dummy_image).STATE == ImageStates.READY)





# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist(one: One):
    image_id    = 999999
    snapshot_id = 0

    with pytest.raises(OneNoExistsException):
        one.image.snapshotdelete(image_id, snapshot_id)




def test_snapshot_not_exist(one: One, dummy_image: int):
    image_id    = dummy_image
    snapshot_id = 99999

    with pytest.raises(OneActionException):
        one.image.snapshotdelete(image_id, snapshot_id)




def test_unactive_snapshot(one: One, image_with_snapshots: int):
    image_id    = image_with_snapshots
    snapshots   = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.PARENT == -1))
    one.image.snapshotrevert(image_id, snapshot_id)
    time.sleep(5)

    snapshots   = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (not snapshot.CHILDREN)))

    _id = one.image.snapshotdelete(image_id, snapshot_id)
    assert _id == snapshot_id
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id not in snapshots_ids




def test_active_snapshot(one: One, image_with_snapshots: int):
    image_id  = image_with_snapshots
    snapshots = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    active_snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.ACTIVE))

    with pytest.raises(OneException):
        one.image.snapshotdelete(image_id, active_snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert active_snapshot_id in snapshots_ids



def test_snapshot_with_children(one: One, image_with_snapshots: int):
    image_id  = image_with_snapshots
    snapshots = one.image.info(image_id).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (snapshot.CHILDREN)))

    with pytest.raises(OneException):
        one.image.snapshotdelete(image_id, snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id in snapshots_ids
