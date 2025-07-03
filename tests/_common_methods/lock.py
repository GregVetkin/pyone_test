import pytest

from pyone     import OneNoExistsException, OneActionException



def lock_if_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.lock(999999, 1, False)


def lock_locked__test(api_object, one_object_id, lock_level, lock_check):
    init_lock_level = api_object.info(one_object_id).LOCK.LOCKED

    if lock_check:
        with pytest.raises(OneActionException):
            api_object.lock(one_object_id, lock_level, lock_check)
        assert api_object.info(one_object_id).LOCK.LOCKED == init_lock_level

    else:
        _id = api_object.lock(one_object_id, lock_level, lock_check)
        assert _id == one_object_id
        assert api_object.info(one_object_id).LOCK.LOCKED == lock_level





def lock_unlocked__test(api_object, one_object_id, lock_level, lock_check):
    assert api_object.info(one_object_id).LOCK is None

    _id = api_object.lock(one_object_id, lock_level, lock_check)
    assert _id == one_object_id

    assert api_object.info(one_object_id).LOCK.LOCKED == lock_level