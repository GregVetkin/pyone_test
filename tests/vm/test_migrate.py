import pytest
import pyone
import time
import random

from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmLcmStates, VmStates, VmRecoverOperations
from config.base        import API_URI, BrestAdmin


MIGRATION_TYPE = [
    0, #save
    1, #poweroff,
    2. #poweroffhard
]


@pytest.fixture
def large_vm(one: One):
    vm_id   = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=999\nMEMORY=999999\n", True)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    one.vm.deploy(vm_id, host_id, False, -1, "")
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    yield vm_id

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)




# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id           = random.randint(9999, 999999)
    host_id         = random.choice([host.ID for host in one.hostpool.info().HOST])
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0
   
    with pytest.raises(pyone.OneNoExistsException):
        one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)



def test_host_not_exist(one: One, poweroff_vm_mini: int):
    vm_id           = poweroff_vm_mini
    host_id         = random.randint(9999, 999999)
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)



def test_datastore_not_exist(one: One, poweroff_vm_mini: int):
    vm_id           = poweroff_vm_mini
    host_id         = random.choice([host.ID for host in one.hostpool.info().HOST])
    live            = False
    host_check      = False
    datastore_id    = random.randint(9999, 999999)
    migration_type  = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)



def test_certain_host(one: One, poweroff_vm_mini: int):
    vm_id           = poweroff_vm_mini
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    _id = one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    assert _id == vm_id
    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID == host_id



def test_certain_datastore(one: One, poweroff_vm_mini: int):
    vm_id           = poweroff_vm_mini
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id     = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id       = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID
    current_ds_tm_mad   = one.datastore.info(current_ds_id, False).TM_MAD
    
    host_id = current_host_id
    datastore_id = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE 
                           if ds.TYPE == 1 and ds.TM_MAD == current_ds_tm_mad and ds.ID != current_ds_id])

    _id = one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, False)

    assert _id == vm_id
    assert vm_info.HISTORY_RECORDS.HISTORY[-1].HID   == host_id
    assert vm_info.HISTORY_RECORDS.HISTORY[-1].DS_ID == datastore_id



@pytest.mark.parametrize("ds_type", [0, 2])
def test_wrong_datastore_type(one: One, poweroff_vm_mini: int, ds_type: int):
    vm_id           = poweroff_vm_mini
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id   = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID
    
    host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    datastore_id = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE if ds.TYPE == ds_type])

    with pytest.raises(pyone.OneInternalException):
        one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID   == current_host_id
    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID == current_ds_id



def test_different_datastore_tm_driver(one: One, poweroff_vm_mini: int):
    vm_id           = poweroff_vm_mini
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id     = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID
    current_ds_id       = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID
    current_ds_tm_mad   = one.datastore.info(current_ds_id, False).TM_MAD

    host_id = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])
    datastore_id = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE 
                                  if ds.TYPE == 1 and ds.TM_MAD != current_ds_tm_mad])

    with pytest.raises(pyone.OneActionException):
        one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID   == current_host_id
    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID == current_ds_id



@pytest.mark.parametrize("host_check", [True, False])
def test_host_capacity_check(one: One, large_vm: int, host_check: bool):
    vm_id           = large_vm
    live            = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID
    host_id  = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    if host_check:
        with pytest.raises(pyone.OneActionException):
            one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

        assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID == current_host_id

    else:
        _id = one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

        assert _id == vm_id
        assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID == host_id



def test_live_migration(one: One, running_vm_mini: int):
    vm_id           = running_vm_mini
    live            = False
    host_check      = False
    datastore_id    = -1
    migration_type  = 0

    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])

    _id = one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type)

    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.PROLOG_MIGRATE)
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)

    assert _id == vm_id
    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID == host_id




@pytest.mark.KERBEROS
@pytest.mark.parametrize("vm_fixture", ["poweroff_vm_mini", "running_vm_mini"])
def test_migration_KERBEROS(vm_fixture: str, request):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = request.getfixturevalue(vm_fixture)
    migration_type = 0
    host_check = False

    vm_info_before = one.vm.info(vm_id, False)

    if vm_info_before.STATE == VmStates.ACTIVE:
        live = True
    else:
        live = False


    current_ds_id = vm_info_before.HISTORY_RECORDS.HISTORY[-1].DS_ID
    current_ds_tm_mad = one.datastore.info(current_ds_id, False).TM_MAD
    datastore_id = random.choice([ds.ID for ds in one.datastorepool.info().DATASTORE 
                                  if ds.TYPE == 1 and ds.TM_MAD == current_ds_tm_mad and ds.ID != current_ds_id])

    current_host_id = next(host.ID for host in one.hostpool.info().HOST if vm_id in host.VMS.ID)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST if current_host_id != host.ID])


    _id = one.vm.migrate(vm_id, host_id, live, host_check, datastore_id, migration_type, False, pw.sessionDir)
    pw.run_one_vm_action()

    if vm_info_before.STATE == VmStates.ACTIVE:
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.MIGRATE)
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)
    else:
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info_after = one.vm.info(vm_id, False)

    assert _id == vm_id
    assert vm_info_after.HISTORY_RECORDS.HISTORY[-1].HID   == host_id
    assert vm_info_after.HISTORY_RECORDS.HISTORY[-1].DS_ID == datastore_id
