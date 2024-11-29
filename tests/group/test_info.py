import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group, group_exist
from config             import ADMIN_NAME

from tests._common_tests.info   import info__test, info_if_not_exist__test


@pytest.fixture
def group():
    _id     = create_group(get_unic_name())
    group   = Group(_id)
    yield group
    group.delete()


# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One):
    info_if_not_exist__test(one.group)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_info_of_current_user(one: One):
    group_info = one.group.info(-1)
    assert group_info.NAME == "brestadmins"


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_info(one: One, group: Group):
    info__test(one.group, group)
