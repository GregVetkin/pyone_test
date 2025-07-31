import pytest

from api                import One
from utils.other        import wait_until
from config.tests       import LOCK_LEVELS

from tests._common_methods.lock     import lock__test, not_exist__test



@pytest.fixture(params=LOCK_LEVELS)
def locked_vm(one: One, dummy_vm: int, request):
    vm_id = dummy_vm
    lock_level  = request.param

    one.vm.lock(vm_id, lock_level, False)
    wait_until(lambda: one.vm.info(vm_id, False).LOCK is not None)

    yield vm_id

    one.vm.unlock(vm_id)
    wait_until(lambda: one.vm.info(vm_id, False).LOCK is None)



# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    not_exist__test(one.vm)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_unlocked(one: One, dummy_vm: int, lock_level: int, lock_check: bool):
    vm_id = dummy_vm
    lock__test(one.vm, vm_id, lock_level, lock_check)

    one.vm.unlock(vm_id)
    wait_until(lambda: one.vm.info(vm_id, False).LOCK is None)




@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_locked(one: One, locked_vm: int, lock_level: int, lock_check: bool):
    vm_id = locked_vm
    lock__test(one.vm, vm_id, lock_level, lock_check)
    

