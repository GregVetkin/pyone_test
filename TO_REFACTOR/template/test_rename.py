import pytest
from api                import One
from utils              import get_unic_name
from one_cli.template   import Template, create_template
from config             import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test




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



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    rename_if_not_exist__test(one.template)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_template(one: One, vmtemplate: Template):
    rename__test(one.template, vmtemplate)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_name_collision(one: One, vmtemplate: Template, vmtemplate_2: Template):
    cant_be_renamed__test(one.template, vmtemplate, vmtemplate_2.info().NAME)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_template_name(one: One, vmtemplate: Template):
    cant_be_renamed__test(one.template, vmtemplate, "")


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_template_name(one: One, vmtemplate: Template, bad_symbol: str):
    cant_be_renamed__test(one.template, vmtemplate, f"{bad_symbol}")
    cant_be_renamed__test(one.template, vmtemplate, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.template, vmtemplate, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.template, vmtemplate, f"Greg{bad_symbol}Vetkin")
