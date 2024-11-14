import pytest

from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template
from config             import BRESTADM, LOCK_LEVELS

from tests._common_tests.lock import lock_if_not_exist__test
from tests._common_tests.lock import lock_unlocked__test
from tests._common_tests.lock import lock_locked__test



BRESTADM_AUTH = get_user_auth(BRESTADM)


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
    if the_template.info().LOCK is not None:
        the_template.unlock()
    the_template.delete()
    


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One, lock_level):
    lock_if_not_exist__test(one.template, lock_level)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_unlocked_template(one: One, vmtemplate: Template, lock_level):
    lock_unlocked__test(one.template, vmtemplate, lock_level)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", LOCK_LEVELS)
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_locked_template(one: One, vmtemplate: Template, init_lock_lvl, lock_level, lock_check):
    vmtemplate.lock(init_lock_lvl)
    lock_locked__test(one.template, vmtemplate, lock_level, lock_check)

