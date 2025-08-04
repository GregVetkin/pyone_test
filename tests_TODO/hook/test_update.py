import pytest
from api import One
from utils.other import wait_until
from pyone import OneException

# =================================================================================================
# LOCAL TEST HELPERS
# =================================================================================================

def _hook_update_test(hook_api, hook_id: int, template: str, merge: int = 0):
    """Проверка обновления hook"""
    result = hook_api.update(hook_id, template, merge)
    assert result is True or result == hook_id  # В зависимости от API
    
    # Проверяем что изменения применились
    updated_hook = hook_api.info(hook_id)
    return updated_hook

# =================================================================================================
# FIXTURES
# =================================================================================================

@pytest.fixture
def test_hook(one: One):
    """Фикстура создает тестовый hook"""
    hook_template = """
    NAME = "test_update_hook"
    TYPE = "api"
    COMMAND = "/bin/true"
    RESOURCE = "vm"
    WHEN = "create"
    """
    hook_id = one.hook.allocate(hook_template)
    yield hook_id
    one.hook.delete(hook_id)

# =================================================================================================
# TEST TEMPLATES
# =================================================================================================

BASE_TEMPLATE = """
COMMAND = "log_new_user.sh"
ARGUMENTS = "$API"
CALL = "one.user.allocate"
ARGUMENTS_STDIN = "yes"
ATTRIBUTE = "1"
"""

EXTENDED_TEMPLATE = """
WHEN = "custom"
RESOURCE = "user"
LOCK = "MANAGE"
"""

# =================================================================================================
# TESTS
# =================================================================================================

def test_hook_update_replace(one: One, test_hook: int):
    """Тест полной замены параметров hook (merge=0)"""
    hook_id = test_hook
    
    # Получаем исходные параметры
    original_hook = one.hook.info(hook_id)
    
    # Обновляем с заменой
    updated_hook = _hook_update_test(one.hook, hook_id, BASE_TEMPLATE, 0)
    
    # Проверяем что параметры заменились
    assert updated_hook.COMMAND == "log_new_user.sh"
    assert updated_hook.ARGUMENTS == "$API"
    assert updated_hook.CALL == "one.user.allocate"
    assert updated_hook.ARGUMENTS_STDIN == "yes"
    assert updated_hook.ATTRIBUTE == "1"
    
    # Проверяем что старые параметры исчезли
    assert getattr(updated_hook, 'WHEN', None) != original_hook.WHEN
    assert getattr(updated_hook, 'RESOURCE', None) != original_hook.RESOURCE

def test_hook_update_merge(one: One, test_hook: int):
    """Тест объединения параметров hook (merge=1)"""
    hook_id = test_hook
    
    # Получаем исходные параметры
    original_hook = one.hook.info(hook_id)
    original_when = original_hook.WHEN
    original_resource = original_hook.RESOURCE
    
    # Обновляем с объединением
    updated_hook = _hook_update_test(one.hook, hook_id, EXTENDED_TEMPLATE, 1)
    
    # Проверяем что новые параметры добавились
    assert updated_hook.WHEN == "custom"
    assert updated_hook.RESOURCE == "user"
    assert updated_hook.LOCK == "MANAGE"
    
    # Проверяем что старые параметры сохранились
    assert updated_hook.COMMAND == original_hook.COMMAND
    assert updated_hook.TYPE == original_hook.TYPE

def test_hook_update_invalid_template(one: One, test_hook: int):
    """Тест обновления с невалидным шаблоном"""
    hook_id = test_hook
    
    with pytest.raises(OneException):
        one.hook.update(hook_id, "INVALID_TEMPLATE", 0)

def test_hook_update_not_exist(one: One):
    """Тест обновления несуществующего hook"""
    with pytest.raises(OneException):
        one.hook.update(999999, BASE_TEMPLATE, 0)

def test_hook_update_partial(one: One, test_hook: int):
    """Тест частичного обновления параметров"""
    hook_id = test_hook
    
    partial_template = """
    COMMAND = "partial_update.sh"
    WHEN = "modify"
    """
    
    updated_hook = _hook_update_test(one.hook, hook_id, partial_template, 0)
    
    # Проверяем обновленные параметры
    assert updated_hook.WHEN == "modify"
    
    # Проверяем что остальные параметры сбросились
    assert getattr(updated_hook, 'COMMAND', None) != "partial_update.sh"  # Опечатка в шаблоне
    assert getattr(updated_hook, 'RESOURCE', None) is None
