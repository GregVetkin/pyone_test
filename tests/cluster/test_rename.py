import pytest
from pyone                          import OneActionException
from api                            import One
from config.tests                   import INVALID_CHARS
from utils.other                    import get_unic_name
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test







def test_cluster_not_exist(one: One):
    not_exist__test(one.cluster)


def test_rename_cluster(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    new_name = get_unic_name()
    
    rename__test(one.cluster, cluster_id, new_name)



def test_name_collision(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    new_name   = one.cluster.info(0, False).NAME

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, new_name)
    


def test_empty_name(one: One, dummy_cluster):
    cluster_id = dummy_cluster
    new_name   = ""

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_cluster, char: str):
    cluster_id = dummy_cluster

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, f"{char}")

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, f"Gregory{char}")

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, f"{char}Vetkin")

    with pytest.raises(OneActionException):
        rename__test(one.cluster, cluster_id, f"Gregory{char}Vetkin")

