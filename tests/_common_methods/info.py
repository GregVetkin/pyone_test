import pytest
from pyone      import OneNoExistsException, OneException





def info_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.info(999999)



def info__test(api_object, one_object_id):
    object_info = api_object.info(one_object_id)
    assert object_info.ID == one_object_id




def cant_be_obtained_info__test(api_object, one_object_id):
    with pytest.raises(OneException):
        api_object.info(one_object_id)
