from api                        import One
from tests._common_methods.info import info_if_not_exist__test
from tests._common_methods.info import info__test





# =================================================================================================
# TESTS
# =================================================================================================



def test_hook_not_exist(one: One):
    info_if_not_exist__test(one.hook)




def test_hook_info(one: One, dummy_hook):
    info__test(one.hook, dummy_hook)


