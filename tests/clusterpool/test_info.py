import pytest

from api                import One
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster
from config             import ADMIN_NAME
from typing             import List






@pytest.fixture
def clusters():
    cluster_list = []
    for _ in range(5):
        cluster_id = create_cluster(get_unic_name())
        cluster    = Cluster(cluster_id)
        cluster_list.append(cluster)

    yield cluster_list

    for cluster in cluster_list:
        cluster.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_show_all_clusters(one: One, clusters: List[Cluster]):
    cluster_ids     = [cluster._id for cluster in clusters]
    clusterpool     = one.clusterpool.info().CLUSTER
    clusterpool_ids = [cluster.ID for cluster in clusterpool]
    
    assert set(cluster_ids).issubset(clusterpool_ids)

