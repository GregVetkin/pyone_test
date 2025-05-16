import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import ADMIN_NAME


@pytest.fixture
def empty_group():
    _id     = create_group(get_unic_name())
    group   = Group(_id)
    yield group
    group.delete()

@pytest.fixture
def user():
    _id     = create_user(name=get_unic_name())
    user    = User(_id)
    yield user
    user.delete()

@pytest.fixture
def group_with_nonadmin_user(empty_group, user):
    user.addgroup(empty_group._id)
    yield empty_group
    user.delgroup(empty_group._id)

@pytest.fixture
def group_with_admin(group_with_nonadmin_user):
    group_with_nonadmin_user.addadmin(group_with_nonadmin_user.info().USERS[0])
    yield group_with_nonadmin_user
    admins = group_with_nonadmin_user.info().ADMINS
    if admins:
        group_with_nonadmin_user.deladmin(admins[0])


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.deladmin(999999, 0)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.deladmin(0, 999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_in_the_group(one: One, empty_group: Group, user: User):
    assert user._id not in empty_group.info().USERS
    with pytest.raises(OneException):
        one.group.deladmin(empty_group._id, user._id)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_an_admin_of_the_group(one: One, group_with_nonadmin_user: Group):
    group_info   = group_with_nonadmin_user.info()
    group_users  = group_info.USERS
    group_admins = group_info.ADMINS
    assert group_users
    assert group_users[0] not in group_admins
    
    with pytest.raises(OneException):
        one.group.deladmin(group_with_nonadmin_user._id, group_users[0])


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_remove_admin_from_the_group(one: One, group_with_admin: Group):
    old_group_info  = group_with_admin.info()
    group_admins    = old_group_info.ADMINS
    assert group_admins
    admin_id = group_admins[0]

    _id = one.group.deladmin(group_with_admin._id, admin_id)
    assert _id == group_with_admin._id
    
    new_group_info = group_with_admin.info()
    assert admin_id not in new_group_info.ADMINS
    assert admin_id in new_group_info.USERS
