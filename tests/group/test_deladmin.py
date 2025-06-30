import pytest

from api        import One
from pyone      import OneNoExistsException, OneActionException, OneInternalException




@pytest.fixture
def group_with_nonadmin_user(one: One, dummy_group: int, dummy_user: int):
    group_id = dummy_group
    user_id  = dummy_user

    one.user.addgroup(user_id, group_id)

    yield group_id

    if user_id in one.group.info(group_id).USERS.ID:
        one.user.delgroup(user_id, group_id)


@pytest.fixture
def group_with_admin(one: One, group_with_nonadmin_user: int):
    group_id = group_with_nonadmin_user
    user_id  = one.group.info(group_id).USERS.ID[0]

    one.group.addadmin(group_id, user_id)

    yield group_id

    for user_id in one.group.info(group_id).ADMINS.ID:
        one.group.deladmin(group_id, user_id)

        

# =================================================================================================
# TESTS
# =================================================================================================




def test_group_not_exist(one: One):
    group_id = 99999
    user_id  = 0

    with pytest.raises(OneNoExistsException):
        one.group.deladmin(group_id, user_id)



def test_user_not_exist(one: One):
    group_id = 0
    user_id  = 99999

    with pytest.raises(OneNoExistsException):
        one.group.deladmin(group_id, user_id)



def test_user_not_in_the_group(one: One, dummy_group: int, dummy_user: int):
    group_id = dummy_group
    user_id  = dummy_user

    assert user_id not in one.group.info(group_id).USERS.ID

    with pytest.raises(OneInternalException):
        one.group.deladmin(group_id, user_id)



def test_user_not_an_admin_of_the_group(one: One, group_with_nonadmin_user: int):
    group_id        = group_with_nonadmin_user
    group_info      = one.group.info(group_id)
    group_user_ids  = group_info.USERS.ID
    group_admin_ids = group_info.ADMINS.ID

    assert group_user_ids
    assert group_user_ids[0] not in group_admin_ids
    user_id = group_user_ids[0]
    
    with pytest.raises(OneInternalException):
        one.group.deladmin(group_id, user_id)



def test_delete_admin_from_the_group(one: One, group_with_admin: int):
    group_id        = group_with_admin
    group_admin_ids = one.group.info(group_id).ADMINS.ID

    assert group_admin_ids
    user_id = group_admin_ids[0]

    _id = one.group.deladmin(group_id, user_id)
    assert _id == group_id
    
    new_group_info = one.group.info(group_id)
    assert user_id not in new_group_info.ADMINS.ID
    assert user_id     in new_group_info.USERS.ID
