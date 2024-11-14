import pytest
import random
from pyone      import OneNoExistsException, OneAuthorizationException, OneActionException




def update_if_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.update(999999, template="", replace=True)

    with pytest.raises(OneNoExistsException):
        api_method.update(999999, template="", replace=False)



def update_and_replace__test(api_method, one_object):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    one_object.update(start_template, append=True)

    # Создание нового шаблона с атрибутами
    new_attributes = [f"ATTR_{_}" for _ in range(1, 3)]
    new_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attributes))

    # API метод обновления шаблона с заменой
    api_method.update(one_object._id, new_template, replace=True)
    one_object_new_template = one_object.info().TEMPLATE

    # Проверка, что стартовые атрибуты пропали из шаблона
    for start_attribute in start_attributes:
        assert start_attribute not in one_object_new_template

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert new_attribute in one_object_new_template



def update_and_merge__test(api_method, one_object):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    one_object.update(start_template, append=True)

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attibutes   = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attibutes))
    attr_template   += updated_attribute

    # API метод обновления шаблона со слиянием
    api_method.update(one_object._id, attr_template, replace=False)
    one_object_new_template = one_object.info().TEMPLATE

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attibutes:
        assert new_attribute in one_object_new_template

    # Проверка, что стартовые атрибуты остались в шаблоне
    for start_attribute in start_attributes:
        assert start_attribute in one_object_new_template
    
    # Проверка, что выбранный атрибут изменил свое значение
    assert one_object_new_template[attribute_name] == new_attribute_value



def update_cant_be_updated__test(api_method, one_object):
    attribute_name = "TEST_ATTR"
    with pytest.raises((OneAuthorizationException, OneActionException)):
        api_method.update(one_object._id, template=f"{attribute_name} = TEST_DATA")
    assert attribute_name not in one_object.info().TEMPLATE
