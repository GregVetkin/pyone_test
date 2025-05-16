from api                            import One
from tests._common_methods.update   import update_and_merge__test
from tests._common_methods.update   import update_and_replace__test
from tests._common_methods.update   import update_if_not_exist__test







def test_cluster_not_exist(one: One):
    update_if_not_exist__test(one.cluster)


def test_update_by_replace(one: One, dummy_cluster):
    update_and_replace__test(one.cluster, dummy_cluster)


def test_update_by_merge(one: One, dummy_cluster):
    update_and_merge__test(one.cluster, dummy_cluster)
