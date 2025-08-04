import pytest
from datetime import datetime, timedelta
from api import One
from utils.other import wait_until
from pyone import OneException

# =================================================================================================
# LOCAL TEST HELPERS
# =================================================================================================

def _hooklog_info_test(hooklog_api, hook_id: int, rc: int = None, 
                      start_date: int = None, end_date: int = None):
    """Проверка получения логов hook"""
    result = hooklog_api.info(hook_id, rc, start_date, end_date)
    
    assert isinstance(result, list)  # Должен возвращаться список записей
    if result:
        assert all(isinstance(item, dict) for item in result)  # Каждая запись - словарь
    return result

# =================================================================================================
# FIXTURES
# =================================================================================================

@pytest.fixture
def executed_hook(one: One):
    """Фикстура создает и выполняет hook для тестирования логов"""
    hook_template = """
    NAME = "test_log_hook"
    TYPE = "api"
    COMMAND = "/bin/true"
    RESOURCE = "vm"
    WHEN = "create"
    """
    hook_id = one.hook.allocate(hook_template)
    
    # Триггерим hook
    one.hook.trigger(hook_id)
    
    # Ждем завершения выполнения
    wait_until(lambda: one.hook.info(hook_id).LAST_EXECUTION_TIME is not None,
              timeout=10,
              interval=1)
    
    yield hook_id
    
    # Удаляем хук после теста
    one.hook.delete(hook_id)

# =================================================================================================
# TESTS
# =================================================================================================

def test_hooklog_basic(one: One, executed_hook: int):
    """Базовый тест получения логов hook"""
    hook_id = executed_hook
    logs = _hooklog_info_test(one.hooklog, hook_id)
    
    # Проверяем что есть хотя бы одна запись
    assert len(logs) >= 1
    
    # Проверяем структуру записи
    log_entry = logs[0]
    assert 'EXECUTION_ID' in log_entry
    assert 'HOOK_ID' in log_entry
    assert 'TIMESTAMP' in log_entry
    assert 'RC' in log_entry

def test_hooklog_with_filters(one: One, executed_hook: int):
    """Тест фильтрации логов по параметрам"""
    hook_id = executed_hook
    
    # Получаем временной диапазон
    end_time = int(datetime.now().timestamp())
    start_time = end_time - 3600  # 1 час назад
    
    # Тестируем разные варианты фильтрации
    test_cases = [
        {'rc': 0, 'desc': 'только успешные выполнения'},
        {'rc': -1, 'desc': 'только ошибки'},
        {'start_date': start_time, 'end_date': end_time, 'desc': 'по временному диапазону'},
        {'rc': 0, 'start_date': start_time, 'end_date': end_time, 'desc': 'комбинированные фильтры'}
    ]
    
    for case in test_cases:
        logs = _hooklog_info_test(
            one.hooklog, 
            hook_id,
            rc=case.get('rc'),
            start_date=case.get('start_date'),
            end_date=case.get('end_date')
        )
        
        # Для проверяемого случая должны получить хотя бы одну запись
        if case['desc'] == 'только успешные выполнения':
            assert len(logs) >= 1
            assert all(log['RC'] == 0 for log in logs)

def test_hooklog_not_exist(one: One):
    """Тест получения логов несуществующего hook"""
    with pytest.raises(OneException):
        one.hooklog.info(999999)

def test_hooklog_empty_result(one: One, executed_hook: int):
    """Тест случая когда нет записей по заданным фильтрам"""
    hook_id = executed_hook
    
    # Берем диапазон дат когда hook еще не выполнялся
    far_past = int((datetime.now() - timedelta(days=365)).timestamp()
    far_future = int((datetime.now() + timedelta(days=365)).timestamp()
    
    logs = _hooklog_info_test(
        one.hooklog,
        hook_id,
        start_date=far_past,
        end_date=far_future,
        rc=42  # Несуществующий код возврата
    )
    
    assert len(logs) == 0
