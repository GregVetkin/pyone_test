import pytest
import pyone
from api                import One
from config.tests       import LOCK_LEVELS
from utils.other        import wait_until

from tests._common_methods.update import update__test, not_exist__test





@pytest.fixture(params=LOCK_LEVELS)
def locked_template(one: One, dummy_template: int, request):
    tempalte_id = dummy_template
    lock_level  = request.param

    one.template.lock(tempalte_id, lock_level, False)
    wait_until(lambda: one.template.info(tempalte_id, False, False).LOCK is not None)

    yield tempalte_id

    one.template.unlock(tempalte_id)
    wait_until(lambda: one.template.info(tempalte_id, False, False).LOCK is None)






# =================================================================================================
# TESTS
# =================================================================================================



def test_template_not_exist(one: One):
    not_exist__test(one.template)


@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_template: int, update_type: int):
    template_id = dummy_template
    update__test(one.template, template_id, update_type)




@pytest.mark.parametrize("update_type", [0, 1])
def test_locked_template(one: One, locked_template: int, update_type: int):
    template_id = locked_template
    lock_level  = one.template.info(template_id).LOCK.LOCKED

    if lock_level == 3:
        update__test(one.template, template_id, update_type)
    else:
        with pytest.raises(pyone.OneException):
            update__test(one.template, template_id,  update_type)

