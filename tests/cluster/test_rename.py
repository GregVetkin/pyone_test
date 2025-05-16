import pytest
from api                            import One
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test






def test_cluster_not_exist(one: One):
    not_exist__test(one.cluster)


def test_rename_cluster(one: One, dummy_cluster):
    rename__test(one.cluster, dummy_cluster)



def test_name_collision(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    taken_name = one.cluster.info(0).NAME
    cant_be_renamed__test(one.cluster, cluster_id, taken_name)
    


def test_empty_name(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    empty_name = ""
    cant_be_renamed__test(one.cluster, cluster_id, empty_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_cluster, char: str):
    cluster_id = dummy_cluster
    cant_be_renamed__test(one.cluster, cluster_id, f"{char}")
    cant_be_renamed__test(one.cluster, cluster_id, f"Gregory{char}")
    cant_be_renamed__test(one.cluster, cluster_id, f"{char}Vetkin")
    cant_be_renamed__test(one.cluster, cluster_id, f"Gregory{char}Vetkin")
