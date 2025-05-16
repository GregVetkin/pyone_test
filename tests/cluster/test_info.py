from api                        import One
from tests._common_methods.info import info_if_not_exist__test
from tests._common_methods.info import info__test





# =================================================================================================
# TESTS
# =================================================================================================



def test_cluster_not_exist(one: One):
    info_if_not_exist__test(one.cluster)




def test_cluster_info(one: One, dummy_cluster):
    info__test(one.cluster, dummy_cluster)

