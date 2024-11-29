import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from config             import ADMIN_NAME
from one_cli.group      import Group, group_exist




# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_group_name(one: One):
    with pytest.raises(OneException):
        one.group.allocate("")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_name_is_taken(one: One):
    with pytest.raises(OneException):
        one.group.allocate(Group(0).info().NAME)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_creation(one: One):
    _id = one.group.allocate(get_unic_name())
    assert group_exist(_id)
    Group(_id).delete()

