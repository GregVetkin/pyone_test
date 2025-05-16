import pytest
import random
import pyone


from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME, VmStates




@pytest.fixture
# @pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def poweroff_vm(one: One):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=1\nMEMORY=1\n")
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.recover(vm_id, 3)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)







# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(pyone.OneNoExistsException):
        one.vm.action("terminate", 999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_action_not_exist(one: One, poweroff_vm: VirtualMachine):
    pass



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_terminate_hard(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_terminate(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_undeploy_hard(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_undeploy(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_poweroff(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_poweroff_hard(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_reboot(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_reboot_hard(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_hold(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_release(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_stop(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_suspend(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_resume(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_resched(one: One):
    pass

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unresched(one: One):
    pass