import pytest

from api                import One
from utils              import get_unic_name
from one_cli.template   import Template, create_template
from config             import ADMIN_NAME, LOCK_LEVELS


from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test
from tests._common_tests.update import cant_be_updated__test



@pytest.fixture
def vmtemplate():
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    _id = create_template(template)
    the_template = Template(_id)
    yield the_template
    if the_template.info().LOCK:
        the_template.unlock()
    the_template.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    update_if_not_exist__test(one.template)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_template__replace(one: One, vmtemplate: Template):
    update_and_replace__test(one.template, vmtemplate)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_template__merge(one: One, vmtemplate: Template):
    update_and_merge__test(one.template, vmtemplate)


@pytest.mark.skip()
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_locked_template(one: One, vmtemplate: Template, lock_level):
    vmtemplate.lock(lock_level)
    if lock_level == 3:
        update_and_replace__test(one.template, vmtemplate)
    else:
        cant_be_updated__test(one.template, vmtemplate)

