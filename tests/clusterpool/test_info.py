import pytest
import random
from api            import One
from utils.other    import get_unic_name




@pytest.fixture
def cluster_ids(one: One):
    cluster_ids_list = []
    for _ in range(random.randint(3, 10)):
        cluster_name = get_unic_name()
        cluster_id   = one.cluster.allocate(cluster_name)
        cluster_ids_list.append(cluster_id)

    yield cluster_ids_list

    for cluster_id in cluster_ids_list:
        one.cluster.delete(cluster_id)






def test_get_all_clusters_info(one: One, cluster_ids):
    clusterpool     = one.clusterpool.info().CLUSTER
    clusterpool_ids = [cluster.ID for cluster in clusterpool]
    
    assert set(cluster_ids).issubset(clusterpool_ids)

