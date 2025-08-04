import pytest
from api import One
from utils.other import wait_until
from pyone import OneException

# =================================================================================================
# LOCAL TEST HELPERS
# =================================================================================================

def _retry_success_test(hook_api, hook_id: int):
    """Проверка успешного выполнения retry"""
    result = hook_api.retry(hook_id)
    assert result is True  # Или hook_id в зависимости от API

def _retry_not_exist_test(hook_api):
    """Проверка обработки несуществующего Hook"""
    with pytest.raises(OneException):
        hook_api.retry(999999)

# =================================================================================================
# FIXTURES
# =================================================================================================

@pytest.fixture
def failed_hook(one: One):
    """Фикстура создает специально проваленный Hook для тестирования retry"""
    hook_template = """
    NAME = "test_failed_hook"
    TYPE = "api"
    COMMAND = "/bin/false"  # Намеренно проваливающаяся команда
    ARGUMENTS = "arg1"
    RESOURCE = "vm"
    WHEN = "create"
    """
    hook_id = one.hook.allocate(hook_template)
    
    # Имитируем провал Hook
    try:
        one.hook.trigger(hook_id)
    except:
        pass
    
    # Ждем пока hook перейдет в состояние ERROR
    wait_until(lambda: one.hook.info(hook_id).STATUS == "ERROR",
              timeout=10,
              interval=1)
    
    yield hook_id
    
    # Удаляем хук после теста
    one.hook.delete(hook_id)

# =================================================================================================
# TESTS
# =================================================================================================

def test_retry_not_exist(one: One):
    """Тест попытки retry несуществующего Hook"""
    _retry_not_exist_test(one.hook)

def test_retry_failed_hook(one: One, failed_hook: int):
    """Тест успешного retry проваленного Hook"""
    hook_id = failed_hook
    
    # Проверяем что Hook действительно в состоянии ошибки
    hook_info = one.hook.info(hook_id)
    assert hook_info.STATUS == "ERROR"
    
    _retry_success_test(one.hook, hook_id)
    
    # Дополнительная проверка что статус изменился после retry
    wait_until(lambda: one.hook.info(hook_id).STATUS != "ERROR",
              timeout=10,
              interval=1)

def test_retry_already_successful_hook(one: One):
    """Тест retry для уже успешного hook"""
    # Создаем успешный hook
    hook_template = """
    NAME = "test_success_hook"
    TYPE = "api"
    COMMAND = "/bin/true"
    RESOURCE = "vm"
    WHEN = "create"
    """
    hook_id = one.hook.allocate(hook_template)
    
    try:
        # Проверяем что retry успешного hook не вызывает ошибок
        _retry_success_test(one.hook, hook_id)
    finally:
        one.hook.delete(hook_id)
