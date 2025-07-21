import pytest

from api                import One
from config.tests       import LOCK_LEVELS
from utils.other        import wait_until

from tests._common_methods.update import update_and_merge__test
from tests._common_methods.update import update_and_replace__test
from tests._common_methods.update import update_if_not_exist__test
from tests._common_methods.update import cant_be_updated__test




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
    update_if_not_exist__test(one.template)



def test_update_template__replace(one: One, dummy_template: int):
    template_id = dummy_template
    update_and_replace__test(one.template, template_id)



def test_update_template__merge(one: One, dummy_template: int):
    template_id = dummy_template
    update_and_merge__test(one.template, template_id)




def test_update_locked_template(one: One, locked_template: int):
    template_id = locked_template
    lock_level = one.template.info(template_id).LOCK.LOCKED

    if lock_level == 3:
        update_and_replace__test(one.template, template_id)
    else:
        cant_be_updated__test(one.template, template_id)

