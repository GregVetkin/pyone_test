import pytest

from api                import One
from pyone              import OneAuthorizationException
from utils              import get_user_auth
from one_cli.template   import Template, create_template
from config             import BRESTADM


from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test
from tests._common_tests.update import update_cant_be_updated__test


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def vmtemplate():
    template = """
        NAME    = api_test_template
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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One):
    update_if_not_exist__test(one.template)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_template__replace(one: One, vmtemplate: Template):
    update_and_replace__test(one.template, vmtemplate)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_template__merge(one: One, vmtemplate: Template):
    update_and_merge__test(one.template, vmtemplate)




#@pytest.mark.skip(reason="Нужна консультация по поводу провала при lock-level 4 (All). И уровне 3")
@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_locked_image(one: One, vmtemplate: Template, lock_level):
    vmtemplate.lock(lock_level)
    update_cant_be_updated__test(one.template, vmtemplate)

