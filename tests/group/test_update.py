import pytest

from api                            import One
from tests._common_methods.update   import update__test, not_exist__test





def test_group_not_exist(one: One):
    not_exist__test(one.host)


@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_group: int, update_type: int):
    group_id = dummy_group
    update__test(one.group, group_id, update_type)

