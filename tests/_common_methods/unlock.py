import pytest
import random
import pyone




def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        api_object.unlock(one_object_id)


def unlock__test(api_object, one_object_id: int):
    _id = api_object.unlock(one_object_id)
    
    assert _id == one_object_id
    assert api_object.info(one_object_id, False).LOCK is None