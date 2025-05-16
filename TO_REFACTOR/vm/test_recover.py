import pytest
import pyone
from time                       import sleep
from api                        import One
from one_cli.vm                 import VirtualMachine
from config                     import ADMIN_NAME, ALSE_VERSION, ADMIN_PASSWORD, VmLcmStates, VmStates
from utils                      import run_command, get_unic_name




@pytest.fixture
# @pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n", False)
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield VirtualMachine(vm_id)

    try:
        one.vm.recover(vm_id, 3)
        while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)
    except:
        pass


@pytest.fixture
# @pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def running_vm(one: One, vm: VirtualMachine):
    vm_id = vm._id

    if ALSE_VERSION > 1.7:
        admin_name = ADMIN_NAME + "@brest.local"

    run_command(f"sshpass -p '{ADMIN_PASSWORD}' ssh {admin_name}@$HOSTNAME \"echo 'Qwe!2345' | kinit {ADMIN_NAME} ; onevm resume {vm._id}\"")
    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: sleep(0.5)
    yield VirtualMachine(vm._id)



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(pyone.OneNoExistsException):
        one.vm.recover(99999, 0)


# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_0_failure(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 0)
    assert _id == vm_id
    sleep(3)
    assert "ERROR" not in one.vm.info(vm_id).USER_TEMPLATE


# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_1_success(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 1)
    assert _id == vm_id
    sleep(3)
    assert "ERROR" not in one.vm.info(vm_id).USER_TEMPLATE


# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_2_retry(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 2)
    assert _id == vm_id
    sleep(3)
    assert "ERROR" not in one.vm.info(vm_id).USER_TEMPLATE


# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_3_delete(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 3)
    assert _id == vm_id
    sleep(3)
    assert one.vm.info(vm_id).STATE == VmStates.DONE



# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_4_delete_recreate(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 4)
    assert _id == vm_id

    while one.vm.info(vm_id).LCM_STATE == VmLcmStates.RUNNING: sleep(0.5)
    assert one.vm.info(vm_id).LCM_STATE == VmLcmStates.CLEANUP_RESUBMIT

    while one.vm.info(vm_id).LCM_STATE != VmLcmStates.RUNNING: sleep(1)
    assert "ERROR" not in one.vm.info(vm_id).USER_TEMPLATE



# TODO: Expand  test case
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_code_5_delete_db(one: One, running_vm: VirtualMachine):
    vm_id   = running_vm._id
    _id     = one.vm.recover(vm_id, 4)
    assert _id == vm_id
    sleep(30)
    assert one.vm.info(vm_id).STATE == VmStates.DONE


