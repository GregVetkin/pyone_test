import pytest
from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template
from config             import BRESTADM, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import rename_unavailable_symbol__test
from tests._common_tests.rename import rename_empty_name__test
from tests._common_tests.rename import rename_collision__test


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


@pytest.fixture
def vmtemplate_2():
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 1
        MEMORY  = 512
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
    rename_if_not_exist__test(one.template)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_rename_template(one: One, vmtemplate: Template):
    rename__test(one.template, vmtemplate)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_name_collision(one: One, vmtemplate: Template, vmtemplate_2: Template):
    rename_collision__test(one.template, vmtemplate, vmtemplate_2)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_empty_template_name(one: One, vmtemplate: Template):
    rename_empty_name__test(one.template, vmtemplate)


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unavailable_symbols_in_template_name(one: One, vmtemplate: Template, bad_symbol: str):
    rename_unavailable_symbol__test(one.template, vmtemplate, bad_symbol)


