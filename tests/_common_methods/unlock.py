import pytest

from pyone     import OneNoExistsException



def unlock_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.unlock(999999)


def unlock__test(api_object, one_object_id):
    _id = api_object.unlock(one_object_id)
    
    assert _id == one_object_id
    assert api_object.info(one_object_id).LOCK is None