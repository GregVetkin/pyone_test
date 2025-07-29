import pytest
import random
from pyone     import OneNoExistsException






def not_exist__test(api_object):
    one_object_id = random.randint(9999, 999999)
    user_id = -1
    group_id = -1

    with pytest.raises(OneNoExistsException):
        api_object.chown(one_object_id, user_id, group_id)


def chown__test(api_object, one_object_id: int, user_id: int, group_id: int):
    old_one_object_info = api_object.info(one_object_id, False)

    result = api_object.chown(one_object_id, user_id, group_id)
    assert result == one_object_id
    
    new_one_object_info = api_object.info(one_object_id, False)

    if user_id == -1:
        assert old_one_object_info.UID == new_one_object_info.UID
    else:
        assert user_id == new_one_object_info.UID

    if group_id == -1:
       assert old_one_object_info.GID == new_one_object_info.GID
    else: 
        assert group_id == new_one_object_info.GID



