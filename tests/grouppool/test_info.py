import pytest
import random
from typing          import List
from api             import One
from utils.other     import get_unic_name






@pytest.fixture
def group_ids(one: One):
    group_ids_list = []
    for _ in range(random.randint(3, 10)):
        group_name  = get_unic_name()
        group_id    = one.group.allocate(group_name)
        group_ids_list.append(group_id)

    yield group_ids_list

    for group_id in group_ids_list:
        one.group.delete(group_id)




def test_get_all_groups_info(one: One, group_ids: List[int]):
    grouppool_ids = [group.ID for group in one.grouppool.info().GROUP]
    assert set(group_ids).issubset(grouppool_ids)
