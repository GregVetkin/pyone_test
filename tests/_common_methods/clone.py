import pytest

from pyone import OneException, OneNoExistsException
from utils.other import get_unic_name



def not_exist__test(api_method):
    object_id  = 99999
    clone_name = get_unic_name()
    with pytest.raises(OneNoExistsException):
        api_method.clone(object_id, clone_name)



def name_collision__test(api_method, one_object_id, taken_name):
    with pytest.raises(OneException):
        api_method.clone(one_object_id, taken_name)



