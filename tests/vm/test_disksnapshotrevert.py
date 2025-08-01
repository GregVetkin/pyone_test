import pytest
import pyone
import random
import time

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
        for _ in range(3):
            one.vm.disksnapshotcreate(vm_id, disk_id, get_unic_name(), pw.sessionDir)
            pw.run_one_vm_action()
            wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    return vm_id






# =================================================================================================
# TESTS
# =================================================================================================




def test_vm_not_exist(one: One):
    vm_id         = random.randint(9999, 999999)
    disk_id       = 0
    snapshot_id   = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.disksnapshotrevert(vm_id, disk_id, snapshot_id)



def test_disk_not_exist(one: One, poweroff_vm_mini: int):
    vm_id         = poweroff_vm_mini
    disk_id       = random.randint(9999, 999999)
    snapshot_id   = 0

    with pytest.raises(pyone.OneActionException):
        one.vm.disksnapshotrevert(vm_id, disk_id, snapshot_id)



def test_snapshot_not_exist(one: One, poweroff_vm_mini: int):
    vm_id         = poweroff_vm_mini
    disk_id       = 0
    snapshot_id   = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.vm.disksnapshotrevert(vm_id, disk_id, snapshot_id)



@pytest.mark.KERBEROS
def test_revert_snapshot_KERBEROS(poweroff_vm_mini_with_disk_snapshots: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id    = poweroff_vm_mini_with_disk_snapshots
    disk_ids = [int(disk["DISK_ID"]) for disk in one.vm.info(vm_id, False).TEMPLATE["DISK"]]
    disk_id  = random.choice(disk_ids)
    
    snapshots_before        = one.vm.info(vm_id, False).SNAPSHOTS
    disk_snapshots_before   = next(_.SNAPSHOT for _ in snapshots_before if _.DISK_ID == disk_id)
    not_active_shapshot_ids = [_.ID for _ in disk_snapshots_before if _.ACTIVE is None]
    
    snapshot_id = random.choice(not_active_shapshot_ids)
    
    reverted_snapshot_id = one.vm.disksnapshotrevert(vm_id, disk_id, snapshot_id, pw.sessionDir)
    pw.run_one_vm_action()

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.DISK_SNAPSHOT_REVERT_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    snapshots_after      = one.vm.info(vm_id, False).SNAPSHOTS
    disk_snapshots_after = next(_.SNAPSHOT for _ in snapshots_after if _.DISK_ID == disk_id)
    reverted_snapshot    = next(_ for _ in disk_snapshots_after if _.ID == snapshot_id)

    assert reverted_snapshot_id == snapshot_id
    assert reverted_snapshot.ACTIVE == "YES"
