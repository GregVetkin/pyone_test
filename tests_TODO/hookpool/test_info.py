import pytest
import random
from api import One
from utils.other import get_unic_name
from pyone import OneException

# =================================================================================================
# FIXTURES
# =================================================================================================

@pytest.fixture
def hook_ids(one: One):
    """Фикстура создает несколько тестовых хуков разных типов"""
    hook_ids_list = []
    hook_types = ["api", "state"]  # Основные типы хуков
    
    for _ in range(random.randint(3, 5)):
        hook_name = get_unic_name()
        hook_type = random.choice(hook_types)
        
        template = f"""
        NAME = "{hook_name}"
        TYPE = {hook_type}
        COMMAND = "/bin/true"
        """
        
        if hook_type == "state":
            template += """
            RESOURCE = "vm"
            WHEN = "create"
            STATE = "ACTIVE"
            LCM_STATE = "RUNNING"
            """
        
        hook_id = one.hook.allocate(template)
        hook_ids_list.append(hook_id)
    
    yield hook_ids_list
    
    # Удаление созданных хуков после тестов
    for hook_id in hook_ids_list:
        try:
            one.hook.delete(hook_id)
        except OneException:
            pass  # На случай если хук уже удален

# =================================================================================================
# TESTS
# =================================================================================================

def test_hookpool_info_structure(one: One):
    """Тест структуры возвращаемых данных hookpool"""
    hookpool = one.hookpool.info()
    
    assert hasattr(hookpool, 'HOOK')
    assert isinstance(hookpool.HOOK, list)
    
    if hookpool.HOOK:  # Если есть хоть один хук в системе
        sample_hook = hookpool.HOOK[0]
        assert hasattr(sample_hook, 'ID')
        assert hasattr(sample_hook, 'NAME')
        assert hasattr(sample_hook, 'TYPE')

def test_hookpool_contains_created_hooks(one: One, hook_ids):
    """Тест что созданные хуки присутствуют в hookpool"""
    hookpool = one.hookpool.info()
    hookpool_ids = [hook.ID for hook in hookpool.HOOK]
    
    # Проверяем что все созданные хуки есть в hookpool
    for hook_id in hook_ids:
        assert hook_id in hookpool_ids

def test_hookpool_filtering(one: One, hook_ids):
    """Тест фильтрации хуков по типу"""
    # Получаем информацию о созданных хуках
    created_hooks = [one.hook.info(hid) for hid in hook_ids]
    
    # Собираем статистику по типам
    type_counts = {}
    for hook in created_hooks:
        type_counts[hook.TYPE] = type_counts.get(hook.TYPE, 0) + 1
    
    # Для каждого типа проверяем фильтрацию
    for hook_type in type_counts:
        filtered = one.hookpool.info(-1, -1, hook_type).HOOK
        assert len(filtered) >= type_counts[hook_type]
        assert all(hook.TYPE == hook_type for hook in filtered)

def test_hookpool_pagination(one: One, hook_ids):
    """Тест постраничного получения хуков"""
    all_hooks = one.hookpool.info().HOOK
    if len(all_hooks) > 2:  # Если достаточно хуков для теста
        # Первая страница (2 хука)
        page1 = one.hookpool.info(2, 0).HOOK
        assert len(page1) == 2
        
        # Вторая страница
        page2 = one.hookpool.info(2, 2).HOOK
        assert len(page2) == 2
        
        # Проверяем что хуки разные
        assert page1[0].ID != page2[0].ID

def test_hookpool_extended_info(one: One, hook_ids):
    """Тест получения расширенной информации о хуках"""
    extended_pool = one.hookpool.info(-1, -1, -1, True).HOOK  # extended=True
    
    if extended_pool:
        sample_hook = extended_pool[0]
        # Проверяем дополнительные атрибуты
        assert hasattr(sample_hook, 'EXECUTION_RECORDS')
        assert hasattr(sample_hook, 'LOCK')
