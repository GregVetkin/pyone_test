import pytest
from time           import sleep
from pyone          import OneNoExistsException
from one_cli.user   import User
from one_cli.group  import Group





def chown_object_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.chown(999999)



def chown_user_not_exist__test(api_method, one_object):
    old_uid = one_object.info().UID
    with pytest.raises(OneNoExistsException):
        api_method.chown(one_object._id, user_id=999999)
    sleep(1)
    new_uid = one_object.info().UID
    assert old_uid == new_uid



def chown_group_not_exist__test(api_method, one_object):
    old_gid = one_object.info().GID
    with pytest.raises(OneNoExistsException):
        api_method.chown(one_object._id, group_id=999999)
    sleep(1)
    new_gid = one_object.info().GID
    assert old_gid == new_gid



def chown_user_and_group_change__test(api_method, one_object, user: User, group: Group):
    api_method.chown(one_object._id, user._id, group._id)
    sleep(1)
    new_one_object_info = one_object.info()
    assert user._id  == new_one_object_info.UID
    assert group._id == new_one_object_info.GID



def chown_user_and_group_not_changed__test(api_method, one_object):
    old_one_object_info = one_object.info()
    api_method.chown(one_object._id)
    sleep(1)
    new_one_object_info = one_object.info()
    assert old_one_object_info.UNAME == new_one_object_info.UNAME
    assert old_one_object_info.GNAME == new_one_object_info.GNAME



def chown_user_change__test(api_method, one_object, user: User):
    old_one_object_info = one_object.info()
    api_method.chown(one_object._id, user_id=user._id)
    sleep(1)
    new_one_object_info = one_object.info()
    assert new_one_object_info.UID == user._id
    assert new_one_object_info.GID == old_one_object_info.GID



def chown_group_change__test(api_method, one_object, group: Group):
    old_one_object_info = one_object.info()
    api_method.chown(one_object._id, group_id=group._id)
    sleep(1)
    new_one_object_info = one_object.info()
    assert new_one_object_info.UID == old_one_object_info.UID
    assert new_one_object_info.GID == group._id
