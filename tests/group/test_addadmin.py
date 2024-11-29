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
    if user._id in empty_group.info().USERS:
        user.delgroup(empty_group._id)


@pytest.fixture
def group_with_admin(group_with_nonadmin_user):
    group_with_nonadmin_user.addadmin(group_with_nonadmin_user.info().USERS[0])
    yield group_with_nonadmin_user
    admins = group_with_nonadmin_user.info().ADMINS
    if admins:
        group_with_nonadmin_user.deladmin(admins[0])




# @pytest.fixture
# def group_with_admin(user):
#     _id     = create_group(get_unic_name())
#     group   = Group(_id)
#     user.addgroup(group._id)
#     group.addadmin(user._id)
#     yield group
#     group.deladmin(user._id)
#     user.delgroup(group._id)
#     group.delete()

# @pytest.fixture
# def group_with_nonadmin_user(user):
#     _id     = create_group(get_unic_name())
#     group   = Group(_id)
#     user.addgroup(group._id)
#     yield group
#     user.delgroup(group._id)
#     group.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.addadmin(999999, 0)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.addadmin(0, 999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_in_the_group(one: One, empty_group: Group, user: User):
    assert user._id not in empty_group.info().USERS
    with pytest.raises(OneException):
        one.group.addadmin(empty_group._id, user._id)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_already_an_admin_of_group(one: One, group_with_admin: Group):
    group_admins = group_with_admin.info().ADMINS
    assert group_admins
    with pytest.raises(OneException):
        one.group.addadmin(group_with_admin._id, group_admins[0])


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_add_admin_to_group(one: One, group_with_nonadmin_user: Group):
    group_info   = group_with_nonadmin_user.info()
    group_users  = group_info.USERS
    group_admins = group_info.ADMINS
    assert group_users
    assert group_users[0] not in group_admins
    
    _id = one.group.addadmin(group_with_nonadmin_user._id, group_users[0])
    assert _id == group_with_nonadmin_user._id
    assert group_users[0] in group_with_nonadmin_user.info().ADMINS



