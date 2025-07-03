import pytest

from pyone     import OneNoExistsException



def unlock_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.delete(999999)


def unlock__test(api_object, one_object_id):
    api_object.unlock(one_object_id)
    assert api_object.info(one_object_id).LOCK is None