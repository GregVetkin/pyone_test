import pytest
import random
from pyone     import OneNoExistsException, OneException




def update_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.update(999999, template="", replace=True)

    with pytest.raises(OneNoExistsException):
        api_object.update(999999, template="", replace=False)



def cant_be_updated__test(api_object, one_object_id):
    attribute_name  = "TEST_ATTR"
    template        = f"{attribute_name} = TEST_DATA"

    with pytest.raises(OneException):
        api_object.update(one_object_id, template)

    assert api_object.info().TEMPLATE.get(attribute_name)



def update_and_replace__test(api_object, one_object_id):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    api_object.update(one_object_id, start_template, False)

    # Создание нового шаблона с атрибутами
    new_attributes = [f"ATTR_{_}" for _ in range(1, 3)]
    new_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attributes))

    # API метод обновления шаблона с заменой
    result = api_object.update(one_object_id, new_template, True)
    assert result == one_object_id

    one_object_new_template = api_object.info(one_object_id).TEMPLATE

    # Проверка, что стартовые атрибуты пропали из шаблона
    for start_attribute in start_attributes:
        assert one_object_new_template.get(start_attribute) is None

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert one_object_new_template.get(new_attribute)



def update_and_merge__test(api_object, one_object_id):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    api_object.update(one_object_id, start_template, False)

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attibutes   = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attibutes))
    attr_template   += updated_attribute

    # API метод обновления шаблона со слиянием
    result = api_object.update(one_object_id, attr_template, False)
    assert result == one_object_id

    one_object_new_template = api_object.info(one_object_id).TEMPLATE

    # Проверка, что новые атрибуты добавлены в шаблон
    for new_attribute in new_attibutes:
        assert one_object_new_template.get(new_attribute)

    # Проверка, что стартовые атрибуты остались в шаблоне
    for start_attribute in start_attributes:
        assert one_object_new_template.get(start_attribute)
    
    # Проверка, что выбранный атрибут изменил свое значение
    assert one_object_new_template[attribute_name] == new_attribute_value



