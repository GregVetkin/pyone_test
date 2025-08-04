import pytest

from api                            import One
from utils.other                    import wait_until
from config.tests                   import LOCK_LEVELS

from tests._common_methods.unlock   import unlock__test
from tests._common_methods.unlock   import unlock_if_not_exist__test

@pytest.fixture(params=LOCK_LEVELS)
def locked_hook(one: One, dummy_hook: int, request):
    hook_id = dummy_hook
    lock_level = request.param

    one.hook.lock(hook_id, lock_level)
    wait_until(lambda: one.hook.info(hook_id, False).LOCK is not None)

    yield hook_id

    one.hook.unlock(hook_id)
    wait_until(lambda: one.hook.info(hook_id, False).LOCK is None)
    
# =================================================================================================
# TESTS
# =================================================================================================
    
def test_hook_not_exist(one: One):
    """Проверка разблокировки несуществующего Hook."""
    unlock_if_not_exist__test(one.hook)


def test_unlocked_hook(one: One, dummy_hook: int):
    """Проверка разблокировки уже разблокированного Hook."""
    hook_id = dummy_hook
    unlock__test(one.hook, hook_id)


def test_locked_hook(one: One, locked_hook: int):
    """Проверка разблокировки заблокированного Hook."""
    hook_id = locked_hook
    assert one.hook.info(hook_id).LOCK is not None
    unlock__test(one.hook, hook_id)
