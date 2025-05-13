import pytest
from pyone     import OneNoExistsException






def object_not_exist__test(api_object):
    with pytest.raises(OneNoExistsException):
        api_object.chown(999999)



def user_not_exist__test(api_object, one_object_id):
    old_uid = api_object.info(one_object_id).UID
    with pytest.raises(OneNoExistsException):
        api_object.chown(one_object_id, user_id=999999)
    new_uid = api_object.info(one_object_id).UID
    assert old_uid == new_uid



def group_not_exist__test(api_object, one_object_id):
    old_gid = api_object.info(one_object_id).GID

    with pytest.raises(OneNoExistsException):
        api_object.chown(one_object_id, group_id=999999)

    new_gid = api_object.info(one_object_id).GID
    assert old_gid == new_gid



def user_and_group_change__test(api_object, one_object_id, user_id, group_id):
    result = api_object.chown(one_object_id, user_id, group_id)
    assert result == one_object_id

    new_one_object_info = api_object.info(one_object_id)
    assert user_id  == new_one_object_info.UID
    assert group_id == new_one_object_info.GID



def user_and_group_not_changed__test(api_object, one_object_id):
    old_one_object_info = api_object.info(one_object_id)

    result = api_object.chown(one_object_id)
    assert result == one_object_id

    new_one_object_info = api_object.info(one_object_id)
    assert old_one_object_info.UNAME == new_one_object_info.UNAME
    assert old_one_object_info.UID   == new_one_object_info.UID
    assert old_one_object_info.GNAME == new_one_object_info.GNAME
    assert old_one_object_info.GID   == new_one_object_info.GID



def user_change__test(api_object, one_object_id, user_id):
    old_one_object_info = api_object.info(one_object_id)

    result = api_object.chown(one_object_id, user_id, -1)
    assert result == one_object_id

    new_one_object_info = api_object.info(one_object_id)
    assert new_one_object_info.UID == user_id
    assert new_one_object_info.GID == old_one_object_info.GID



def group_change__test(api_object, one_object_id, group_id):
    old_one_object_info = api_object.info(one_object_id)

    result = api_object.chown(one_object_id, -1, group_id)
    assert result == one_object_id

    new_one_object_info = api_object.info(one_object_id)
    assert new_one_object_info.UID == old_one_object_info.UID
    assert new_one_object_info.GID == group_id
