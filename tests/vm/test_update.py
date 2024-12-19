import pytest
import random

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME
from pyone              import OneException



@pytest.fixture()
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.update(999999, template="", replace=True)

    with pytest.raises(OneException):
        one.vm.update(999999, template="", replace=False)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_vm__replace(one: One, vm: VirtualMachine):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    vm.update(start_template, append=True)

    # Создание нового шаблона с атрибутами
    new_attributes = [f"ATTR_{_}" for _ in range(1, 3)]
    new_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attributes))

    # API метод обновления шаблона с заменой
    _id = one.vm.update(vm._id, new_template, replace=True)
    assert _id == vm._id
    one_object_new_template = one.vm.info(vm._id).USER_TEMPLATE

    # Проверка, что стартовые атрибуты пропали из шаблона
    for start_attribute in start_attributes:
        assert start_attribute not in one_object_new_template

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert new_attribute in one_object_new_template




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_vm__merge(one: One, vm: VirtualMachine):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    vm.update(start_template, append=True)

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attibutes   = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attibutes))
    attr_template   += updated_attribute

    # API метод обновления шаблона со слиянием
    _id = one.vm.update(vm._id, attr_template, replace=False)
    assert _id == vm._id
    one_object_new_template = one.vm.info(vm._id).USER_TEMPLATE

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attibutes:
        assert new_attribute in one_object_new_template

    # Проверка, что стартовые атрибуты остались в шаблоне
    for start_attribute in start_attributes:
        assert start_attribute in one_object_new_template
    
    # Проверка, что выбранный атрибут изменил свое значение
    assert one_object_new_template[attribute_name] == new_attribute_value


