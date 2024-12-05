import pytest

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.unlock   import unlock_locked__test
from tests._common_tests.unlock   import unlock_unlocked__test
from tests._common_tests.unlock   import unlock_if_not_exist__test




@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=False)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    unlock_if_not_exist__test(one.vm)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_unlocked_vm(one: One, vm: VirtualMachine):
    unlock_unlocked__test(one.vm, vm)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_locked_template(one: One, vm: VirtualMachine, lock_level):
    vm.lock(lock_level)
    unlock_locked__test(one.vm, vm)

