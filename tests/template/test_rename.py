import pytest
from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test







@pytest.fixture
def take_vmtemplate_name(one: One):
    name = get_unic_name()
    template = f"NAME = {name}"
    _id = one.template.allocate(template)
    yield name
    one.template.delete(_id)



# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    not_exist__test(one.template)



def test_rename(one: One, dummy_template: int):
    rename__test(one.template, dummy_template)



def test_name_collision(one: One, dummy_template: int, take_vmtemplate_name: str):
    cant_be_renamed__test(one.template, dummy_template, take_vmtemplate_name)



def test_empty_name(one: One, dummy_template: int):
    cant_be_renamed__test(one.template, dummy_template, "")


@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_template: int, char: str):
    cant_be_renamed__test(one.template, dummy_template, f"{char}")
    cant_be_renamed__test(one.template, dummy_template, f"Greg{char}")
    cant_be_renamed__test(one.template, dummy_template, f"{char}Vetkin")
    cant_be_renamed__test(one.template, dummy_template, f"Greg{char}Vetkin")
