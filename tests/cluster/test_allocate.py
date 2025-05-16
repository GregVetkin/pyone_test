import pytest
import pyone
from api            import One
from utils.other    import get_unic_name
from config.tests   import INVALID_CHARS




def test_create_cluster(one: One):
    cluster_name = get_unic_name()
    cluster_id   = one.cluster.allocate(cluster_name)
    assert cluster_name == one.cluster.info(cluster_id).NAME
    one.cluster.delete(cluster_id)



def test_name_is_taken(one: One, dummy_cluster: int):
    cluster_id   = dummy_cluster
    cluster_name = one.cluster.info(cluster_id, False).NAME
    
    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate(cluster_name)



def test_empty_name(one: One):
    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate("")



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, char: str):
    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate(f"{char}")

    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate(f"{char}Vetkin")
    
    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate(f"Greg{char}")
    
    with pytest.raises(pyone.OneInternalException):
        one.cluster.allocate(f"Greg{char}Vetkin")

