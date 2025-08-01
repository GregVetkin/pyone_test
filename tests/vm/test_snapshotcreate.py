import pytest
import pyone
import time
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
    vm_id = random.randint(9999, 999999)
    name  = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.snapshotcreate(vm_id, name)




# def test_create_snapshot(one: One, running_vm_mini: int):
#     vm_id            = running_vm_mini
#     snapshot_name    = get_unic_name()
    
#     template_before = one.vm.info(vm_id, True).TEMPLATE

#     if "SNAPSHOT" not in template_before:
#         snapshots_before = []
#         next_snapshot_id = 0
        
#     elif isinstance(template_before["SNAPSHOT"], dict):
#         snapshots_before = [template_before["SNAPSHOT"]]
#         next_snapshot_id = int(template_before["SNAPSHOT"]["SNAPSHOT_ID"]) + 1
        
#     else:
#         snapshots_before = template_before["SNAPSHOT"]
#         next_snapshot_id = max([int(_["SNAPSHOT_ID"] for _ in snapshots_before)]) + 1
        

#     _id = one.vm.snapshotcreate(vm_id, snapshot_name)

#     wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT)
#     wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)

#     assert _id == next_snapshot_id

#     template_after = one.vm.info(vm_id, True).TEMPLATE

#     if "SNAPSHOT" not in template_after:
#         raise Exception(f"Снепшот не был создан. VM_ID: {vm_id}")
        
#     elif isinstance(template_after["SNAPSHOT"], dict):
#         snapshots_after = [template_after["SNAPSHOT"]]

#     else:
#         snapshots_after = template_after["SNAPSHOT"]


#     new_snapshot = next(_ for _ in snapshots_after if _["SNAPSHOT_ID"] == str(_id))

#     assert new_snapshot["NAME"] == snapshot_name
#     assert len(snapshots_after) - len(snapshots_before) == 1






@pytest.mark.KERBEROS
def test_create_snapshot_KERBEROS(running_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id            = running_vm_mini
    snapshot_name    = get_unic_name()
    
    template_before = one.vm.info(vm_id, True).TEMPLATE

    if "SNAPSHOT" not in template_before:
        snapshots_before = []
        next_snapshot_id = 0
        
    elif isinstance(template_before["SNAPSHOT"], dict):
        snapshots_before = [template_before["SNAPSHOT"]]
        next_snapshot_id = int(template_before["SNAPSHOT"]["SNAPSHOT_ID"]) + 1
        
    else:
        snapshots_before = template_before["SNAPSHOT"]
        next_snapshot_id = max([int(_["SNAPSHOT_ID"] for _ in snapshots_before)]) + 1
        

    _id = one.vm.snapshotcreate(vm_id, snapshot_name, pw.sessionDir)
    pw.run_one_vm_action()

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.HOTPLUG_SNAPSHOT)
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)

    assert _id == next_snapshot_id

    template_after = one.vm.info(vm_id, True).TEMPLATE

    if "SNAPSHOT" not in template_after:
        raise Exception(f"Снепшот не был создан. VM_ID: {vm_id}")
        
    elif isinstance(template_after["SNAPSHOT"], dict):
        snapshots_after = [template_after["SNAPSHOT"]]

    else:
        snapshots_after = template_after["SNAPSHOT"]


    new_snapshot = next(_ for _ in snapshots_after if _["SNAPSHOT_ID"] == str(_id))

    assert new_snapshot["NAME"] == snapshot_name
    assert len(snapshots_after) - len(snapshots_before) == 1

