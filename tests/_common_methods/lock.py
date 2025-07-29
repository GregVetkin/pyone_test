import pytest
import random

from pyone          import OneNoExistsException, OneActionException
from utils.other    import wait_until
from utils.version  import Version
from config.base    import BREST_VERSION




def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)
    lock_level = 1
    lock_check = False

    with pytest.raises(OneNoExistsException):
        api_object.lock(one_object_id, lock_level, lock_check)



def lock__test(api_object, one_object_id: int, lock_level: int, lock_check: bool):
    if api_object.info(one_object_id, False).LOCK is None:
        __was_locked__test(api_object, one_object_id, lock_level, lock_check)
    else:
        ___wasnt_locked__test(api_object, one_object_id, lock_level, lock_check)





def __was_locked__test(api_object, one_object_id: int, lock_level: int, lock_check: bool):
    if lock_check:
        init_lock_level = api_object.info(one_object_id, False).LOCK.LOCKED

        with pytest.raises(OneActionException):
            api_object.lock(one_object_id, lock_level, lock_check)

        assert api_object.info(one_object_id).LOCK.LOCKED == init_lock_level

    else:
        ___wasnt_locked__test(api_object, one_object_id, lock_level, lock_check)


def ___wasnt_locked__test(api_object, one_object_id: int, lock_level: int, lock_check: bool):
        _id = api_object.lock(one_object_id, lock_level, lock_check)
        assert _id == one_object_id

        # from brest 4 lock level 4 equals 1 (use)
        if Version(BREST_VERSION) >= Version("4") and lock_level == 4:
            lock_level = 1
            
        assert api_object.info(one_object_id).LOCK.LOCKED == lock_level







