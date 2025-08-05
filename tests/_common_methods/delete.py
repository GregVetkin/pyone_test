import pytest
import random
import time

from pyone  import OneNoExistsException, OneActionException, OneException





def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        api_object.delete(one_object_id)


def delete__test(api_object, one_object_id: int):
    _id = api_object.delete(one_object_id)
    assert _id == one_object_id

    time.sleep(3)
    
    with pytest.raises(OneNoExistsException):
        api_object.info(one_object_id, False)


