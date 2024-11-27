import pytest
from api                import One
from utils              import get_unic_name
from one_cli.cluster    import Cluster, create_cluster
from config             import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test






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
    rename_if_not_exist__test(one.cluster)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_cluster(one: One, cluster: Cluster):
    rename__test(one.cluster, cluster)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_name_collision(one: One, cluster: Cluster):
    cant_be_renamed__test(one.cluster, cluster, "default")
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_cluster_name(one: One, cluster: Cluster):
    cant_be_renamed__test(one.cluster, cluster, "")



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_cluster_name(one: One, cluster: Cluster, bad_symbol: str):
    cant_be_renamed__test(one.cluster, cluster, f"{bad_symbol}")
    cant_be_renamed__test(one.cluster, cluster, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.cluster, cluster, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.cluster, cluster, f"Greg{bad_symbol}Vetkin")
