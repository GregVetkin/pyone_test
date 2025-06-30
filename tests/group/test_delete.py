import pytest

from api                import One

from tests._common_methods.delete import delete__test
from tests._common_methods.delete import delete_if_not_exist__test
from tests._common_methods.delete import cant_be_deleted__test



@pytest.fixture
def group_with_user(one: One, dummy_group: int, dummy_user: int):
    one.user.addgroup(dummy_user, dummy_group)
    yield dummy_group
    one.user.delgroup(dummy_user, dummy_group)



# =================================================================================================
# TESTS
# =================================================================================================


def test_group_not_exist(one: One):
    delete_if_not_exist__test(one.group)



def test_not_empty_group(one: One, group_with_user: int):
    group_id = group_with_user
    assert one.group.info(group_id).USERS.ID
    cant_be_deleted__test(one.group, group_id)



def test_empty_group(one: One, dummy_group: int):
    group_id = dummy_group
    assert not one.group.info(group_id).USERS.ID
    delete__test(one.group, group_id)


def test_system_groups(one: One):
    cant_be_deleted__test(one.group, 0)
    cant_be_deleted__test(one.group, 1)
