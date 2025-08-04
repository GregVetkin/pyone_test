import pytest

from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test

@pytest.fixture
def taken_hook_name(one: One):
    hook_name = get_unic_name()
    hook_template = f"""
        NAME = "{hook_name}"
        TYPE = "api"
        COMMAND = "/usr/bin/true"
        ARGUMENTS = "arg1"
        RESOURCE = "vm"
        WHEN = "create"
    """
    hook_id = one.hook.allocate(hook_template)
    
    yield hook_name
    
    one.hook.delete(hook_id, force=True)
    

# =================================================================================================
# TESTS
# =================================================================================================

def test_hook_not_exist(one: One):
    """Проверка переименования несуществующего Hook."""
    not_exist__test(one.hook)


def test_rename_hook(one: One, dummy_hook: int):
    """Проверка стандартного переименования Hook."""
    hook_id = dummy_hook
    rename__test(one.hook, hook_id)


def test_name_collision(one: One, dummy_hook: int, taken_hook_name: str):
    """Проверка конфликта имён при переименовании."""
    hook_id = dummy_hook
    taken_name = taken_hook_name
    cant_be_renamed__test(one.hook, hook_id, taken_name)


def test_empty_hook_name(one: One, dummy_hook: int):
    """Проверка пустого имени."""
    hook_id = dummy_hook
    cant_be_renamed__test(one.hook, hook_id, "")


@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_hook: int, char: str):
    """Проверка недопустимых символов в имени."""
    hook_id = dummy_hook
    cant_be_renamed__test(one.hook, hook_id, f"{char}")
    cant_be_renamed__test(one.hook, hook_id, f"Hook{char}")
    cant_be_renamed__test(one.hook, hook_id, f"{char}Test")
    cant_be_renamed__test(one.hook, hook_id, f"Hook{char}Test")
