import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group, group_exist
from config             import ADMIN_NAME



@pytest.fixture
def empty_group():
    _id     = create_group(get_unic_name())
    group   = Group(_id)
    yield group
    if group_exist(_id):
        group.delete()

@pytest.fixture
def user():
    _id     = create_user(name=get_unic_name())
    user    = User(_id)
    yield user
    user.delete()

@pytest.fixture
def group_with_user(empty_group, user):
    user.addgroup(empty_group._id)
    yield empty_group
    user.delgroup(empty_group._id)



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.delete(999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_not_empty_group(one: One, group_with_user: Group):
    assert group_with_user.info().USERS
    with pytest.raises(OneException):
        one.group.delete(group_with_user._id)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_an_empty_group(one: One, empty_group: Group):
    assert not empty_group.info().USERS
    assert group_exist(empty_group._id)
    _id = one.group.delete(empty_group._id)
    assert _id == empty_group._id
    assert not group_exist(empty_group._id)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_system_group(one: One):
    system_group = Group(0)
    assert group_exist(system_group._id)
    with pytest.raises(OneException):
        one.group.delete(system_group._id)
    assert group_exist(system_group._id)
