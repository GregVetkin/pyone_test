import pytest
import random

from pyone import OneNoExistsException





def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)

    with pytest.raises(OneNoExistsException):
        api_object.info(one_object_id, False)



def info__test(api_object, one_object_id: int):
    object_info = api_object.info(one_object_id, False)
    assert object_info.ID == one_object_id



