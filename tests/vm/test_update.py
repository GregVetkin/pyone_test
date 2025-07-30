import pytest
import random
import pyone
import time


from api                import One

from utils.commands     import run_command_via_ssh, check_ping
from utils.connection   import brest_admin_ssh_conn, local_admin_ssh_conn
from utils.kerberos     import PyoneWrap
from utils.other        import wait_until, get_unic_name
from utils.version      import Version

from config.base        import API_URI, BrestAdmin, BREST_VERSION
from config.opennebula  import VmStates, VmLcmStates, VmRecoverOperations, VmActions







# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("update_type", [0, 1])
def test_vm_not_exist(one: One, update_type: int):
    vm_id    = random.randint(9999, 999999)
    template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.update(vm_id, template, update_type)





@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_vm: int, update_type: int):
    vm_id = dummy_vm

    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    one.vm.update(vm_id, start_template, 1)

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attributes  = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attributes))
    attr_template   += updated_attribute


    # API метод обновления шаблона со слиянием
    _id = one.vm.update(vm_id, attr_template, update_type)
    assert _id == vm_id
    vm_user_template = one.vm.info(vm_id, False).USER_TEMPLATE


    # Новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert new_attribute in vm_user_template

    if update_type == 0:
        # Cтартовые атрибуты пропали из шаблона (кроме обновленного)
        for start_attribute in start_attributes:
            if start_attribute == attribute_name:
                continue
            assert start_attribute not in vm_user_template

    else:
        # Стартовые атрибуты остались в шаблоне
        for start_attribute in start_attributes:
            assert start_attribute in vm_user_template

    
    # Обновляемый атрибут изменил свое значение
    assert vm_user_template[attribute_name] == new_attribute_value




@pytest.mark.KERBEROS
@pytest.mark.parametrize("update_type", [0, 1])
def test_update_KERBEROS(dummy_vm: int, update_type: int):
    pw    = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one   = pw.get_client()
    vm_id = dummy_vm


    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    one.vm.update(vm_id, start_template, 1, pw.sessionDir)
    pw.run_one_vm_action()

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attributes  = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attributes))
    attr_template   += updated_attribute


    # API метод обновления шаблона со слиянием
    _id = one.vm.update(vm_id, attr_template, update_type, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id
    vm_user_template = one.vm.info(vm_id, False).USER_TEMPLATE


    # Новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert new_attribute in vm_user_template

    if update_type == 0:
        # Cтартовые атрибуты пропали из шаблона (кроме обновленного)
        for start_attribute in start_attributes:
            if start_attribute == attribute_name:
                continue
            assert start_attribute not in vm_user_template

    else:
        # Стартовые атрибуты остались в шаблоне
        for start_attribute in start_attributes:
            assert start_attribute in vm_user_template
    
    # Обновляемый атрибут изменил свое значение
    assert vm_user_template[attribute_name] == new_attribute_value
