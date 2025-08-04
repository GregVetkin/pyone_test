import pytest
import pyone

from api            import One
from utils.other    import get_unic_name
from config.tests   import INVALID_CHARS

from tests._common_methods.rename   import rename__test, not_exist__test




@pytest.fixture
def take_vmtemplate_name(one: One):
    name = get_unic_name()
    template = f"NAME = {name}"
    template_id = one.template.allocate(template)
    yield name
    one.template.delete(template_id, False)



# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    not_exist__test(one.template)



def test_rename(one: One, dummy_template: int):
    template_id = dummy_template
    new_name    = get_unic_name()

    rename__test(one.template, template_id, new_name)



def test_name_is_taken(one: One, dummy_template: int, take_vmtemplate_name: str):
    template_id = dummy_template
    new_name    = take_vmtemplate_name

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, new_name)



def test_empty_name(one: One, dummy_template: int):
    template_id = dummy_template
    new_name    = ""

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_template: int, char: str):
    template_id = dummy_template

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, f"{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, f"Greg{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, f"{char}Vetkin")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.template, template_id, f"Greg{char}Vetkin")

