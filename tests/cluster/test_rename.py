import pytest
from api                            import One
from config.config                         import BAD_SYMBOLS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test




# =================================================================================================
# TESTS
# =================================================================================================



def test_cluster_not_exist(one: One):
    not_exist__test(one.cluster)


def test_rename_cluster(one: One, dummy_cluster):
    rename__test(one.cluster, dummy_cluster)



def test_cluster_name_collision(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    taken_name = one.cluster.info(0).NAME
    cant_be_renamed__test(one.cluster, cluster_id, taken_name)
    


def test_empty_cluster_name(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    empty_name = ""
    cant_be_renamed__test(one.cluster, cluster_id, empty_name)



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
def test_unavailable_symbols_in_cluster_name(one: One, dummy_cluster, bad_symbol: str):
    cluster_id = dummy_cluster
    cant_be_renamed__test(one.cluster, cluster_id, f"{bad_symbol}")
    cant_be_renamed__test(one.cluster, cluster_id, f"Gregory{bad_symbol}")
    cant_be_renamed__test(one.cluster, cluster_id, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.cluster, cluster_id, f"Gregory{bad_symbol}Vetkin")
