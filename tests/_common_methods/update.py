import pytest
import random
from pyone     import OneNoExistsException, OneException




def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)
    template = ""
    
    for update_type in [0, 1]:
        with pytest.raises(OneNoExistsException):
            api_object.update(one_object_id, template, update_type)



def update__test(api_object, one_object_id: int, update_type: int):
    # Создание стартовых атрибутов в шаблоне объекта, которые будут проверяться
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    api_object.update(one_object_id, start_template, 1)

    # Выбор атрибута, у которого будет заменено значение новым атрибутом
    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    # Создание нового шаблона с атрибутами и обновляемым атрибутом
    new_attributes  = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attributes))
    attr_template   += updated_attribute


    # API метод обновления шаблона со слиянием
    _id = api_object.update(one_object_id, attr_template, update_type)
    assert _id == one_object_id
    result_template = api_object.info(one_object_id, False).TEMPLATE


    # Новые атрибуты добавлены в шаблон
    for new_attribute in new_attributes:
        assert new_attribute in result_template

    if update_type == 0:
        # Cтартовые атрибуты пропали из шаблона (кроме обновленного)
        for start_attribute in start_attributes:
            if start_attribute == attribute_name:
                continue
            assert start_attribute not in result_template

    elif update_type == 1:
        # Стартовые атрибуты остались в шаблоне
        for start_attribute in start_attributes:
            assert start_attribute in result_template
    
    # Обновляемый атрибут изменил свое значение
    assert result_template[attribute_name] == new_attribute_value




def cant_be_updated__test(api_object, one_object_id):
    attribute_name  = "TEST_ATTR"
    template        = f"{attribute_name} = TEST_DATA"

    with pytest.raises(OneException):
        api_object.update(one_object_id, template, True)
    
    with pytest.raises(OneException):
        api_object.update(one_object_id, template, False)

    assert not api_object.info(one_object_id).TEMPLATE.get(attribute_name)
