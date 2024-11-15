import pytest

from api                import One
from utils              import get_unic_name
from one_cli.template   import Template, create_template
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.unlock   import unlock_locked__test
from tests._common_tests.unlock   import unlock_unlocked__test
from tests._common_tests.unlock   import unlock_if_not_exist__test




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
    the_template.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    unlock_if_not_exist__test(one.template)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_unlocked_template(one: One, vmtemplate: Template):
    unlock_unlocked__test(one.template, vmtemplate)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_locked_template(one: One, vmtemplate: Template, lock_level):
    vmtemplate.lock(lock_level)
    unlock_locked__test(one.template, vmtemplate)

