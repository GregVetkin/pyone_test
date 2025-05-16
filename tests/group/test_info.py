from api                            import One
from tests._common_methods.info     import info_if_not_exist__test
from tests._common_methods.info     import info__test





def test_group_not_exist(one: One):
    info_if_not_exist__test(one.group)



def test_group_info_of_current_user(one: One):
    group_info = one.group.info(-1)
    assert group_info.NAME == "brestadmins"



def test_group_info(one: One, dummy_group):
    info__test(one.group, dummy_group)
