import pytest
import pyone
import random

from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmLcmStates, VmStates
from config.base        import API_URI, BrestAdmin


# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id         = random.randint(9999, 999999)
    disk_id       = 0
    snapshot_name = get_unic_name()

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.disksnapshotcreate(vm_id, disk_id, snapshot_name)




def test_disk_not_exist(one: One, poweroff_vm_mini: int):
    vm_id         = poweroff_vm_mini
    disk_id       = random.randint(9999, 999999)
    snapshot_name = get_unic_name()

    with pytest.raises(pyone.OneActionException):
        one.vm.disksnapshotcreate(vm_id, disk_id, snapshot_name)
    


# возможные комбинации
def test_create_disk_snapshot(one: One, poweroff_vm_mini: int):
    vm_id         = poweroff_vm_mini # можно будет добавить и запущенную вм
    disk_id       = 0                # можно будет добавить выбор случайного диска у вм. НО и лучше добавить проверку, что снепшоты других дисков не тронуты
    snapshot_name = get_unic_name()

    disk_snapshots_before       = next((_.SNAPSHOT for _ in one.vm.info(vm_id, False).SNAPSHOTS if _.DISK_ID == disk_id), [])
    max_disk_snapshot_id_before = max([_.ID for _ in disk_snapshots_before], default=-1)
    disk_active_snapshot_id_before = next((_ for _ in disk_snapshots_before if _.ACTIVE == "YES"), None)

    created_snapshot_id = one.vm.disksnapshotcreate(vm_id, disk_id, snapshot_name)

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE in [VmLcmStates.DISK_SNAPSHOT_POWEROFF, VmLcmStates.DISK_SNAPSHOT])
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    disk_snapshots_after       = next((_.SNAPSHOT for _ in one.vm.info(vm_id, False).SNAPSHOTS if _.DISK_ID == disk_id), [])
    max_disk_snapshot_id_after = max([_.ID for _ in disk_snapshots_after], default=-1)

    assert created_snapshot_id == max_disk_snapshot_id_after
    assert len(disk_snapshots_after) - len(disk_snapshots_before) == 1
    assert max_disk_snapshot_id_after - max_disk_snapshot_id_before == 1
    
    new_snapshot = next(_ for _ in disk_snapshots_after if _.ID == created_snapshot_id)

    assert new_snapshot.ACTIVE == "YES"
    assert new_snapshot.NAME   == snapshot_name


    if len(disk_snapshots_before) == 0:
        assert new_snapshot.PARENT == -1
    else:
        assert new_snapshot.PARENT == disk_active_snapshot_id_before




@pytest.mark.KERBEROS
def test_create_disk_snapshot_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id         = poweroff_vm_mini # можно будет добавить и запущенную вм
    disk_id       = 0                # можно будет добавить выбор случайного диска у вм
    snapshot_name = get_unic_name()

    disk_snapshots_before       = next((_.SNAPSHOT for _ in one.vm.info(vm_id, False).SNAPSHOTS if _.DISK_ID == disk_id), [])
    max_disk_snapshot_id_before = max([_.ID for _ in disk_snapshots_before], default=-1)
    disk_active_snapshot_id_before = next((_ for _ in disk_snapshots_before if _.ACTIVE == "YES"), None)

    created_snapshot_id = one.vm.disksnapshotcreate(vm_id, disk_id, snapshot_name, pw.sessionDir)
    pw.run_one_vm_action()

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE in [VmLcmStates.DISK_SNAPSHOT_POWEROFF, VmLcmStates.DISK_SNAPSHOT])
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    disk_snapshots_after       = next((_.SNAPSHOT for _ in one.vm.info(vm_id, False).SNAPSHOTS if _.DISK_ID == disk_id), [])
    max_disk_snapshot_id_after = max([_.ID for _ in disk_snapshots_after], default=-1)

    assert created_snapshot_id == max_disk_snapshot_id_after
    assert len(disk_snapshots_after) - len(disk_snapshots_before) == 1
    assert max_disk_snapshot_id_after - max_disk_snapshot_id_before == 1
    
    new_snapshot = next(_ for _ in disk_snapshots_after if _.ID == created_snapshot_id)

    assert new_snapshot.ACTIVE == "YES"
    assert new_snapshot.NAME   == snapshot_name


    if len(disk_snapshots_before) == 0:
        assert new_snapshot.PARENT == -1
    else:
        assert new_snapshot.PARENT == disk_active_snapshot_id_before
