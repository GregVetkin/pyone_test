import pytest
import random

from pyone  import OneNoExistsException, OneActionException, OneException





def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        api_object.delete(one_object_id)


def delete__test(api_object, one_object_id: int):
    _id = api_object.delete(one_object_id)
    assert _id == one_object_id

    with pytest.raises(OneNoExistsException):
        api_object.info(one_object_id, False)


