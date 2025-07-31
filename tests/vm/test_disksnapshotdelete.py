import pytest
import pyone
import random

from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmLcmStates, VmStates
from config.base        import API_URI, BrestAdmin






@pytest.fixture
def poweroff_vm_mini_with_disk_snapshots(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id    = poweroff_vm_mini
    image_id = one.vm.info(vm_id, False).TEMPLATE["DISK"]["IMAGE_ID"]

    for _ in range(2):
        one.vm.attach(vm_id, f"DISK=[IMAGE_ID={image_id}]", pw.sessionDir)
        pw.run_one_vm_action()
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    
    disk_ids = [int(disk["DISK_ID"]) for disk in one.vm.info(vm_id, False).TEMPLATE["DISK"]]

    for disk_id in disk_ids:
        for _ in range(8):
            snapshot_id = one.vm.disksnapshotcreate(vm_id, disk_id, get_unic_name(), pw.sessionDir)
            pw.run_one_vm_action()
            wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

            if _ != 0 and _ % 2 == 0:
                snapshot_id_to_revert = snapshot_id - random.randint(1, _)
                one.vm.disksnapshotrevert(vm_id, disk_id, snapshot_id_to_revert, pw.sessionDir)
                pw.run_one_vm_action()
                wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.DISK_SNAPSHOT_REVERT_POWEROFF)
                wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    return vm_id







# =================================================================================================
# TESTS
# =================================================================================================




# def test_vm_not_exist(one: One):
#     vm_id       = random.randint(9999, 999999)
#     disk_id     = 0
#     snapshot_id = 0

#     with pytest.raises(pyone.OneException):
#         one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)


# def test_disk_not_exist(one: One, poweroff_vm_mini: int):
#     vm_id       = poweroff_vm_mini
#     disk_id     = random.randint(9999, 999999)
#     snapshot_id = 0

#     with pytest.raises(pyone.OneActionException):
#         one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)


# def test_disksnapshot_not_exist(one: One, poweroff_vm_mini: int):
#     vm_id       = poweroff_vm_mini
#     disk_id     = 0
#     snapshot_id = random.randint(9999, 999999)

#     with pytest.raises(pyone.OneActionException):
#         one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)
    





def test_delete_disk_snapshot(one: One, poweroff_vm_mini_with_disk_snapshots: int):
    vm_id          = poweroff_vm_mini_with_disk_snapshots
    disk_ids       = [int(disk["DISK_ID"]) for disk in one.vm.info(vm_id, False).TEMPLATE["DISK"]]
    target_disk_id = random.choice(disk_ids)
    
    snapshots_before = one.vm.info(vm_id, False).SNAPSHOTS
    total_snapshots_before = sum([len(_.SNAPSHOT) for _ in snapshots_before])

    disk_snapshots_before = next(_.SNAPSHOT for _ in snapshots_before if _.DISK_ID == target_disk_id)
    total_disk_snapshots_before = len(disk_snapshots_before)

    removable_shapshot_ids = [_.ID for _ in disk_snapshots_before if _.CHILDREN is None and _.ACTIVE is None]
    target_snapshot_id = random.choice(removable_shapshot_ids)

    deleted_snapshot_id = one.vm.disksnapshotdelete(vm_id, target_disk_id, target_snapshot_id)

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.DISK_SNAPSHOT_DELETE_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    
    snapshots_after = one.vm.info(vm_id, False).SNAPSHOTS
    total_snapshots_after = sum([len(_.SNAPSHOT) for _ in snapshots_after])

    disk_snapshots_after = next(_.SNAPSHOT for _ in snapshots_after if _.DISK_ID == target_disk_id)
    total_disk_snapshots_after = len(disk_snapshots_after)

    assert target_snapshot_id == deleted_snapshot_id
    assert deleted_snapshot_id not in [_.ID for _ in disk_snapshots_after]
    assert (total_disk_snapshots_before - total_disk_snapshots_after) == 1
    assert (total_snapshots_before - total_snapshots_after) == 1
    
    # добавить проверку, что родителя удаленного снепшота в CHILDREN больше нет id удаленного снепшота
