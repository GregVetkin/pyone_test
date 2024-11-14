import pytest

from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template
from config             import BRESTADM

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test


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
    the_template.delete()
    


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One):
    info_if_not_exist__test(one.template)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_info(one: One, vmtemplate: Template):
    info__test(one.template, vmtemplate)

