import pytest
from pyone     import OneNoExistsException






def unlock_if_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.unlock(99999)


def unlock_locked__test(api_method, one_object):
    assert hasattr(one_object.info(), "LOCK")
    api_method.unlock(one_object._id)
    assert not hasattr(one_object.info(), "LOCK")


def unlock_unlocked__test(api_method, one_object):
    assert not hasattr(one_object.info(), "LOCK")
    api_method.unlock(one_object._id)
    assert not hasattr(one_object.info(), "LOCK")


    