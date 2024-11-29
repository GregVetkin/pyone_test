import pytest

from api             import One
from utils           import get_unic_name
from one_cli.group   import Group, create_group
from config          import ADMIN_NAME

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test



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
    update_if_not_exist__test(one.host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_group__replace(one: One, group: Group):
    update_and_replace__test(one.group, group)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_group__merge(one: One, group: Group):
    update_and_merge__test(one.group, group)

