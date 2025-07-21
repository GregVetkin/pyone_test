import pytest

from api                            import One
from utils.other                    import wait_until
from config.tests                   import LOCK_LEVELS
from tests._common_methods.unlock   import unlock__test
from tests._common_methods.unlock   import unlock_if_not_exist__test




@pytest.fixture(params=LOCK_LEVELS)
def locked_template(one: One, dummy_template: int, request):
    tempalte_id = dummy_template
    lock_level  = request.param

    one.template.lock(tempalte_id, lock_level, False)
    wait_until(lambda: one.template.info(tempalte_id, False).LOCK is not None)

    yield tempalte_id

    one.template.unlock(tempalte_id)
    wait_until(lambda: one.template.info(tempalte_id, False).LOCK is None)








# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    unlock_if_not_exist__test(one.template)




def test_unlock_unlocked(one: One, dummy_template: int):
    template_id = dummy_template
    unlock__test(one.template, template_id)



def test_unlock_locked(one: One, locked_template: int):
    template_id = locked_template
    unlock__test(one.template, template_id)

