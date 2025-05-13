import pytest

from api            import One
from pyone          import OneException
from utils.other    import get_unic_name




# =================================================================================================
# TESTS
# =================================================================================================




def test_name_is_taken(one: One):
    taken_name = one.clusterpool.info().CLUSTER[0].NAME
    with pytest.raises(OneException):
        one.cluster.allocate(taken_name)




def test_name_is_empty(one: One):
    with pytest.raises(OneException):
        one.cluster.allocate("")




def test_create_cluster(one: One):
    cluster_name = get_unic_name()
    cluster_id   = one.cluster.allocate(cluster_name)
    assert cluster_name == one.cluster.info(cluster_id).NAME
    one.cluster.delete(cluster_id)

