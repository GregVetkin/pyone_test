from api                            import One
from tests._common_methods.info     import not_exist__test, info__test




    




def test_host_not_exist(one: One):
    not_exist__test(one.host)



def test_host_info(one: One, dummy_host):
    host_id = dummy_host
    info__test(one.host, host_id)
