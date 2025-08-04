import pytest

from api                            import One
from utils.other                    import wait_until
from config.tests                   import LOCK_LEVELS
from tests._common_methods.unlock   import unlock__test, not_exist__test





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




def test_unlock_unlocked(one: One, dummy_vm: int):
    vm_id = dummy_vm
    unlock__test(one.vm, vm_id)



def test_unlock_locked(one: One, locked_vm: int):
    vm_id = locked_vm
    unlock__test(one.vm, vm_id)
