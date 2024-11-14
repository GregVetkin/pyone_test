import pytest
from pyone      import OneNoExistsException, OneActionException, OneAuthorizationException






def lock_if_not_exist__test(api_method, lock_level):
    with pytest.raises(OneNoExistsException):
        api_method.lock(999999, lock_level)




def lock_unlocked__test(api_method, one_object, lock_level):
    assert one_object.info().LOCK == None
    api_method.lock(one_object._id, lock_level)
    assert one_object.info().LOCK.LOCKED == lock_level




def lock_locked__test(api_method, one_object, lock_level, lock_check):
    start_info = one_object.info()
    assert start_info.LOCK is not None

    if lock_check:
        with pytest.raises(OneActionException):
            api_method.lock(one_object._id, lock_level=lock_level, check_already_locked=lock_check)
        assert one_object.info().LOCK.LOCKED == start_info.LOCK.LOCKED
    else:
        api_method.lock(one_object._id, lock_level=lock_level, check_already_locked=lock_check)
        assert one_object.info().LOCK.LOCKED == lock_level
