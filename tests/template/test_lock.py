import pytest

from api                import One
from utils.other        import wait_until
from config.tests       import LOCK_LEVELS

from tests._common_methods.lock import lock__test, not_exist__test




@pytest.fixture(params=LOCK_LEVELS)
def locked_template(one: One, dummy_template: int, request):
    template_id = dummy_template
    lock_level  = request.param

    one.template.lock(template_id, lock_level, False)
    wait_until(lambda: one.template.info(template_id, False, False).LOCK is not None)

    yield template_id

    one.template.unlock(template_id)
    wait_until(lambda: one.template.info(template_id, False, False).LOCK is None)




# =================================================================================================
# TESTS
# =================================================================================================


def test_template_not_exist(one: One):
    not_exist__test(one.template)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_unlocked(one: One, dummy_template: int, lock_level: int, lock_check: bool):
    template_id = dummy_template
    lock__test(one.template, template_id, lock_level, lock_check)

    one.template.unlock(template_id)
    wait_until(lambda: one.template.info(template_id, False).LOCK is None)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_locked(one: One, locked_template: int, lock_level: int, lock_check: bool):
    template_id = locked_template
    lock__test(one.template, template_id, lock_level, lock_check)
    

