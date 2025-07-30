from api                            import One
from tests._common_methods.info     import info__test, not_exist__test





def test_group_not_exist(one: One):
    not_exist__test(one.group)



def test_current_user_group(one: One):
    group_id = -1
    group_info = one.group.info(group_id, False)

    assert group_info.NAME == "brestadmins"
    assert group_info.ID == 0



def test_group_info(one: One, dummy_group):
    info__test(one.group, dummy_group)
