import pytest

from api                import One
from utils.other        import wait_until
from config.tests       import LOCK_LEVELS

from tests._common_methods.lock import lock_if_not_exist__test
from tests._common_methods.lock import lock_unlocked__test
from tests._common_methods.lock import lock_locked__test

@pytest.fixture(params=LOCK_LEVELS)
def locked_hook(one: One, dummy_hook: int, request):
    hook_id = dummy_hook
    lock_level = request.param

    one.hook.lock(hook_id, lock_level, False)
    wait_until(lambda: one.hook.info(hook_id, False).LOCK is not None)

    yield hook_id

    one.hook.unlock(hook_id)  # Разблокируем Hook
    wait_until(lambda: one.hook.info(hook_id).LOCK is None)



# =================================================================================================
# TESTS
# =================================================================================================

def test_hook_not_exist(one: One):
    """Проверка обработки несуществующего Hook."""
    lock_if_not_exist__test(one.hook)


@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_unlocked_hook(one: One, dummy_hook: int, lock_level: int, lock_check: bool):
    """Проверка блокировки разблокированного Hook."""
    hook_id = dummy_hook
    lock_unlocked__test(one.hook, hook_id, lock_level, lock_check)

    one.hook.unlock(hook_id)
    wait_until(lambda: one.hook.info(hook_id).LOCK is None)


@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_locked_hook(one: One, locked_hook: int, lock_level: int, lock_check: bool):
    """Проверка повторной блокировки уже заблокированного Hook."""
    hook_id = locked_hook
    lock_locked__test(one.hook, hook_id, lock_level, lock_check)
