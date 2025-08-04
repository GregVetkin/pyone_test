import pytest
import random
import time
import pyone

from api                import One
from utils.other        import wait_until
from utils.version      import Version
from config.opennebula  import VmStates, ImageStates, VmRecoverOperations
from config.base        import BREST_VERSION




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
        one.image.snapshotrevert(image_id, snapshot_id)



def test_snapshot_not_exist(one: One, dummy_image: int):
    image_id    = dummy_image
    snapshot_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.image.snapshotrevert(image_id, snapshot_id)



def test_unactive_snapshot(one: One, image_with_snapshots: int):
    image_id                = image_with_snapshots
    snapshots               = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    unactive_snapshots_ids  = [snapshot.ID for snapshot in snapshots if not snapshot.ACTIVE]
    snapshot_id             = random.choice(unactive_snapshots_ids)

    _id = one.image.snapshotrevert(image_id, snapshot_id)
    assert _id == snapshot_id
    time.sleep(5)

    snapshots               = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    active_snapshot_id      = next(snapshot.ID for snapshot in snapshots if snapshot.ACTIVE)
    assert active_snapshot_id == snapshot_id



@pytest.mark.xfail(
        Version(BREST_VERSION) < Version("4"),
        raises=pyone.OneActionException,
        reason="Тест ожидаемо провален. Запрещен откат активного снимка в Брест 3.х"
)
def test_active_snapshtot(one: One, image_with_snapshots: int):
    image_id            = image_with_snapshots
    snapshots           = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    active_snapshot_id  = next(snapshot.ID for snapshot in snapshots if snapshot.ACTIVE)

    _id = one.image.snapshotrevert(image_id, active_snapshot_id)
    assert _id == active_snapshot_id
    time.sleep(5)

    snapshots               = one.image.info(image_id, False).SNAPSHOTS.SNAPSHOT
    new_active_snapshot_id  = next(snapshot.ID for snapshot in snapshots if snapshot.ACTIVE)
    assert active_snapshot_id == new_active_snapshot_id
