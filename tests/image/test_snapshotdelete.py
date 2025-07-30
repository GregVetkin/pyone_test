import pytest
import pyone
import time
import random
from config.opennebula  import VmStates, ImageStates, VmRecoverOperations
from api                import One
from utils.other        import wait_until




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
    image_id    = random.randint(9999, 999999)
    snapshot_id = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.image.snapshotdelete(image_id, snapshot_id)




def test_snapshot_not_exist(one: One, dummy_image: int):
    image_id    = dummy_image
    snapshot_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.image.snapshotdelete(image_id, snapshot_id)




def test_unactive_snapshot(one: One, image_with_snapshots: int):
    image_id    = image_with_snapshots
    snapshots   = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.PARENT == -1))
    one.image.snapshotrevert(image_id, snapshot_id)
    time.sleep(5)

    snapshots   = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (not snapshot.CHILDREN)))

    _id = one.image.snapshotdelete(image_id, snapshot_id)
    assert _id == snapshot_id
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id not in snapshots_ids




def test_active_snapshot(one: One, image_with_snapshots: int):
    image_id  = image_with_snapshots
    snapshots = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    active_snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.ACTIVE))

    with pytest.raises(pyone.OneException):
        one.image.snapshotdelete(image_id, active_snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT]
    assert active_snapshot_id in snapshots_ids



def test_snapshot_with_children(one: One, image_with_snapshots: int):
    image_id  = image_with_snapshots
    snapshots = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (snapshot.CHILDREN)))

    with pytest.raises(pyone.OneException):
        one.image.snapshotdelete(image_id, snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id in snapshots_ids
