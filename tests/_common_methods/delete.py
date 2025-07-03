import pytest
from pyone     import OneNoExistsException, OneActionException, OneException





def delete_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.delete(999999)


def delete__test(api_object, one_object_id):
    result = api_object.delete(one_object_id)
    assert result == one_object_id

    with pytest.raises(OneNoExistsException):
        api_object.info(one_object_id)


def cant_be_deleted__test(api_object, one_object_id):
    with pytest.raises((OneActionException, OneException)):
        api_object.delete(one_object_id)
    
    api_object.info(one_object_id)
    
