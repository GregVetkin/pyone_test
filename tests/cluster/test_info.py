import pytest

from api                import One
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster
from config             import ADMIN_NAME

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test



@pytest.fixture
def cluster():
    cluster_id = create_cluster(get_unic_name())
    cluster    = Cluster(cluster_id)
    yield cluster
    cluster.delete()
    


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One):
    info_if_not_exist__test(one.cluster)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_info(one: One, cluster: Cluster):
    info__test(one.cluster, cluster)

