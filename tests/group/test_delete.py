import pytest

from api                import One
from utils              import get_unic_name
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group, group_exist
from config             import ADMIN_NAME

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test



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
    delete_if_not_exist__test(one.group)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_not_empty_group(one: One, group_with_user: Group):
    assert group_with_user.info().USERS
    cant_be_deleted__test(one.group, group_with_user)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_an_empty_group(one: One, empty_group: Group):
    assert not empty_group.info().USERS
    delete__test(one.group, empty_group)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_system_group(one: One):
    cant_be_deleted__test(one.group, Group(0))
