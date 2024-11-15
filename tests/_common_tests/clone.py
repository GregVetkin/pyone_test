import pytest
from pyone      import OneException, OneNoExistsException
from utils      import get_unic_name




def clone_if_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.clone(999999, get_unic_name())



def clone_name_collision__test(api_method, one_object):
    with pytest.raises(OneException):
        api_method.clone(one_object._id, one_object.info().NAME)
    

