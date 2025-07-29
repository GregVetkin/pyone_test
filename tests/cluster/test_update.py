import pytest

from api                            import One
from tests._common_methods.update   import update__test
from tests._common_methods.update   import not_exist__test








def test_cluster_not_exist(one: One):
    not_exist__test(one.cluster)


@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_cluster: int, update_type: int):
    cluter_id = dummy_cluster
    update__test(one.cluster, cluter_id, update_type)

