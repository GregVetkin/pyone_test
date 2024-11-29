import pytest
from typing          import List
from api             import One
from utils           import get_unic_name
from one_cli.group   import Group, create_group
from config          import ADMIN_NAME




@pytest.fixture
def groups():
    group_list = [Group(create_group(get_unic_name())) for _ in range(5)]
    yield group_list
    for group in group_list:
        group.delete()


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_show_all_groups(one: One, groups: List[Group]):
    group_ids      = [group.info().ID for group in groups]
    grouppool       = one.grouppool.info().GROUP
    grouppool_ids   = [group.ID for group in grouppool]
    
    assert set(group_ids).issubset(grouppool_ids)
