import pytest
from api import One
from pyone import OneException
from utils import get_unic_name
from config import ADMIN_NAME

# =================================================================================================
# TEST TEMPLATES
# =================================================================================================

BASE_HOOK_TEMPLATE = """
NAME = "{name}"
TYPE = api
COMMAND = "example.sh"
ARGUMENTS = "$ID"
RESOURCE = vm
WHEN = create
"""

XML_HOOK_TEMPLATE = """
<HOOK>
  <NAME>{name}</NAME>
  <TYPE>api</TYPE>
  <COMMAND>example.sh</COMMAND>
  <ARGUMENTS>$ID</ARGUMENTS>
  <RESOURCE>vm</RESOURCE>
  <WHEN>create</WHEN>
</HOOK>
"""

# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_hook(one: One):
    """Тест создания hook с минимальным набором параметров"""
    template = BASE_HOOK_TEMPLATE.format(name=get_unic_name())
    hook_id = one.hook.allocate(template)
    
    try:
        hook_info = one.hook.info(hook_id)
        assert hook_info.NAME == template.split('NAME = "')[1].split('"')[0]
        assert hook_info.TYPE == "api"
        assert hook_info.COMMAND == "example.sh"
    finally:
        one.hook.delete(hook_id)

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_hook_by_xml(one: One):
    """Тест создания hook с использованием XML-шаблона"""
    template = XML_HOOK_TEMPLATE.format(name=get_unic_name())
    hook_id = one.hook.allocate(template)
    
    try:
        hook_info = one.hook.info(hook_id)
        assert hook_info.NAME in template
        assert hook_info.TYPE == "api"
    finally:
        one.hook.delete(hook_id)

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_required_attributes(one: One):
    """Тест проверки обязательных атрибутов"""
    # Без NAME
    with pytest.raises(OneException):
        one.hook.allocate("""
        TYPE = api
        COMMAND = "test.sh"
        """)
    
    # Без TYPE
    with pytest.raises(OneException):
        one.hook.allocate(f"""
        NAME = "{get_unic_name()}"
        COMMAND = "test.sh"
        """)
    
    # Без COMMAND для TYPE=api
    with pytest.raises(OneException):
        one.hook.allocate(f"""
        NAME = "{get_unic_name()}"
        TYPE = api
        """)

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_hook_types(one: One):
    """Тест создания hook разных типов"""
    for hook_type in ["api", "state"]:  # Основные типы hooks
        template = f"""
        NAME = "{get_unic_name()}"
        TYPE = {hook_type}
        COMMAND = "test_{hook_type}.sh"
        """
        
        if hook_type == "state":
            template += """
            RESOURCE = vm
            WHEN = create
            STATE = ACTIVE
            LCM_STATE = RUNNING
            """
        
        hook_id = one.hook.allocate(template)
        
        try:
            hook_info = one.hook.info(hook_id)
            assert hook_info.TYPE == hook_type
        finally:
            one.hook.delete(hook_id)

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_hook_with_arguments(one: One):
    """Тест создания hook с аргументами"""
    template = BASE_HOOK_TEMPLATE.format(name=get_unic_name()) + """
    ARGUMENTS_STDIN = yes
    """
    
    hook_id = one.hook.allocate(template)
    
    try:
        hook_info = one.hook.info(hook_id)
        assert hook_info.ARGUMENTS_STDIN == "yes"
    finally:
        one.hook.delete(hook_id)
