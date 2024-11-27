import pytest

from api                import One
from pyone              import OneException
from utils              import get_unic_name
from one_cli.cluster    import Cluster, cluster_exist
from config             import ADMIN_NAME






# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_name_is_taken(one: One):
    with pytest.raises(OneException):
        one.cluster.allocate("default")



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_name_is_empty(one: One):
    with pytest.raises(OneException):
        one.cluster.allocate("")



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_create_cluster(one: One):
    _id = one.cluster.allocate(get_unic_name())
    assert cluster_exist(_id)
    Cluster(_id).delete()

