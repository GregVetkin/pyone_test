import pytest
import pyone
import random
from api                            import One
from tests._common_methods.chown    import chown__test, not_exist__test





def test_template_not_exist(one: One):
    not_exist__test(one.template)




def test_user_not_exist(one: One, dummy_template: int):
    template_id = dummy_template
    user_id     = random.randint(9999, 999999)
    group_id    = -1

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.template, template_id, user_id, group_id)





def test_group_not_exist(one: One, dummy_template: int):
    template_id = dummy_template
    user_id     = -1
    group_id    = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.template, template_id, user_id, group_id)





def test_user_and_group_change(one: One, dummy_template: int, dummy_user: int, dummy_group: int):
    template_id = dummy_template
    user_id     = dummy_user
    group_id    = dummy_group
    chown__test(one.template, template_id, user_id, group_id)




def test_user_and_group_not_changed(one: One, dummy_template: int):
    template_id = dummy_template
    user_id     = -1
    group_id    = -1
    chown__test(one.template, template_id, user_id, group_id)




def test_only_user_change(one: One, dummy_template: int, dummy_user: int):
    template_id = dummy_template
    user_id     = dummy_user
    group_id    = -1
    chown__test(one.template, template_id, user_id, group_id)




def test_only_group_change(one: One, dummy_template: int, dummy_group: int):
    template_id = dummy_template
    user_id     = -1
    group_id    = dummy_group
    chown__test(one.template, template_id, user_id, group_id)
