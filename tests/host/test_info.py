from api                            import One
from tests._common_methods.info     import info_if_not_exist__test
from tests._common_methods.info     import info__test




    




def test_host_not_exist(one: One):
    info_if_not_exist__test(one.host)



def test_host_info(one: One, dummy_host):
    info__test(one.host, dummy_host)
