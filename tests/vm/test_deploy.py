import pytest
import random
import pyone


from api                import One

from utils.other        import get_unic_name, wait_until
from utils.kerberos     import PyoneWrap

from config.opennebula  import VmStates, VmActions, VmRecoverOperations
from config.base        import API_URI, BrestAdmin




@pytest.fixture
def undeployed_vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n", False)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    one.vm.action(VmActions.UNDEPLOY_HARD, vm_id)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.UNDEPLOYED)

    yield vm_id

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)



@pytest.fixture
def large_hold_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=99999\nMEMORY=1\n", True)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.HOLD)

    yield vm_id

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)


@pytest.fixture
def hold_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", True)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.HOLD)

    yield vm_id

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)




# =================================================================================================
# TESTS
# =================================================================================================




def test_vm_not_exist(one: One):
    vm_id = random.randint(9999, 999999)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    host_check = False
    datastore_id = random.choice([datastore.ID for datastore in one.datastorepool.info().DATASTORE])
    network_template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)



def test_host_not_exist(one: One, hold_vm: int):
    vm_id = hold_vm
    host_id = random.randint(9999, 999999)
    host_check = False
    datastore_id = random.choice([datastore.ID for datastore in one.datastorepool.info().DATASTORE])
    network_template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)



def test_datastore_not_exist(one: One, hold_vm: int):
    vm_id = hold_vm
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    host_check = False
    datastore_id = random.randint(9999, 999999)
    network_template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)





@pytest.mark.parametrize("vm_fixture_name", [
    "hold_vm",
    "undeployed_vm"
])
def test_deploy_vm(one: One, vm_fixture_name: str, request):
    vm_id = request.getfixturevalue(vm_fixture_name)
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    host_check = False
    datastore_id = -1
    network_template = ""

    _id = one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    assert vm_id in one.host.info(host_id, False).VMS.ID





@pytest.mark.parametrize("host_check", [
    False,
    pytest.param(True, marks=pytest.mark.xfail(raises=pyone.OneActionException)),
])
def test_check_host_capacity(one: One, large_hold_vm: int, host_check: bool):
    vm_id = large_hold_vm
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    datastore_id = -1
    network_template = ""

    _id = one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)
    assert _id == vm_id




def test_certain_datastore(one: One, hold_vm: int):
    vm_id = hold_vm
    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    host_check = False
    datastore_id = random.choice([datastore.ID for datastore in one.datastorepool.info().DATASTORE if datastore.TYPE == 1])
    network_template = ""

    _id = one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template)
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    assert one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].DS_ID == datastore_id




@pytest.mark.KERBEROS
def test_deploy_vm_KERBEROS():
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", True, pw.sessionDir)
    pw.run_one_vm_action()
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.HOLD)


    host_id = random.choice([host.ID for host in one.hostpool.info().HOST])
    host_check = False
    datastore_id = -1
    network_template = ""
    from_shed = False # какой-то еще один опциональный параметр, инфа от Артема Григораша

    _id = one.vm.deploy(vm_id, host_id, host_check, datastore_id, network_template, from_shed,  pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    assert vm_id in one.host.info(host_id, False).VMS.ID

    one.vm.action(VmActions.TERMINATE_HARD, vm_id, pw.sessionDir)
    pw.run_one_vm_action()
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)