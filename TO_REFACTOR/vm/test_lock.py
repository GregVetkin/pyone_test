import pytest

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.lock import lock_if_not_exist__test
from tests._common_tests.lock import lock_unlocked__test
from tests._common_tests.lock import lock_locked__test




@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=False)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One, lock_level):
    lock_if_not_exist__test(one.vm, lock_level)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_lock_unlocked_template(one: One, vm: VirtualMachine, lock_level):
    vm.unlock()
    lock_unlocked__test(one.vm, vm, lock_level)


@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", LOCK_LEVELS)
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_lock_locked_template(one: One, vm: VirtualMachine, init_lock_lvl, lock_level, lock_check):
    vm.lock(init_lock_lvl)
    lock_locked__test(one.vm, vm, lock_level, lock_check)

