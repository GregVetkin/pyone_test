import pytest
from pyone      import OneNoExistsException, OneException





def info_if_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.info(999999)



def info__test(api_method, one_object):
    api_info  = api_method.info(one_object._id)
    cli_info  = one_object.info()
    
    assert cli_info.ID    == api_info.ID
    assert cli_info.NAME  == api_info.NAME



def cant_be_obtained_info__test(api_method, one_object):
    with pytest.raises(OneException):
        api_method.info(one_object._id)
