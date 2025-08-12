import pytest
import pyone
import time
import random

from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmLcmStates, VmStates
from config.base        import API_URI, BrestAdmin





@pytest.fixture
def vm_with_snapshots(running_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = running_vm_mini

    for _ in range(random.randint(1, 5)):
        one.vm.snapshotcreate(vm_id, get_unic_name(), pw.sessionDir)
        pw.run_one_vm_action()

        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT)
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)

    return vm_id





# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id = random.randint(9999, 999999)
    snapshot_id = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.snapshotdelete(vm_id, snapshot_id)



def test_snapshot_not_exist(one: One, dummy_vm: int):
    vm_id = dummy_vm
    snapshot_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.vm.snapshotdelete(vm_id, snapshot_id)




@pytest.mark.KERBEROS
def test_delete_snapshot_KERBEROS(vm_with_snapshots: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = vm_with_snapshots
    template_before = one.vm.info(vm_id, True).TEMPLATE

    if "SNAPSHOT" not in template_before:
        raise Exception(f"Отсутствуют снепшоты у ВМ. VM_ID:{vm_id}")
        
    elif isinstance(template_before["SNAPSHOT"], dict):
        snapshots_before = [template_before["SNAPSHOT"]]

    else:
        snapshots_before = template_before["SNAPSHOT"]

    snapshot_ids_before = [int(_["SNAPSHOT_ID"]) for _ in snapshots_before]
    target_snapshot_id  = random.choice(snapshot_ids_before)


    _id = one.vm.snapshotdelete(vm_id, target_snapshot_id, pw.sessionDir)
    pw.run_one_vm_action()

    time.sleep(5)
    # wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT)
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)

    template_after = one.vm.info(vm_id, True).TEMPLATE

    if "SNAPSHOT" not in template_after:
        snapshots_after = []
        
    elif isinstance(template_after["SNAPSHOT"], dict):
        snapshots_after = [template_after["SNAPSHOT"]]

    else:
        snapshots_after = template_after["SNAPSHOT"]

    snapshot_ids_after = [int(_["SNAPSHOT_ID"]) for _ in snapshots_after]

    assert len(snapshot_ids_after) - len(snapshot_ids_before) == -1
    assert target_snapshot_id not in snapshot_ids_after
    assert _id == vm_id, "Возвращает -1, по документации должно возвращать VM_ID. Создать баг."
    
    