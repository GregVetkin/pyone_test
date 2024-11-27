import pytest

from api                import One
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster
from config             import ADMIN_NAME

from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test




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
    update_if_not_exist__test(one.cluster)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_cluster__replace(one: One, cluster: Cluster):
    update_and_replace__test(one.cluster, cluster)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_update_datastore__merge(one: One, cluster: Cluster):
    update_and_merge__test(one.cluster, cluster)

