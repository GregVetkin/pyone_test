import pytest

from api                            import One
from tests._common_methods.chown    import object_not_exist__test
from tests._common_methods.chown    import user_not_exist__test
from tests._common_methods.chown    import group_not_exist__test
from tests._common_methods.chown    import user_and_group_change__test
from tests._common_methods.chown    import user_and_group_not_changed__test
from tests._common_methods.chown    import user_change__test
from tests._common_methods.chown    import group_change__test






# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    object_not_exist__test(one.template)




def test_user_not_exist(one: One, dummy_template: int):
    template_id = dummy_template
    user_not_exist__test(one.template, template_id)




def test_group_not_exist(one: One, dummy_template: int):
    template_id = dummy_template
    group_not_exist__test(one.template, template_id)




def test_template_user_and_group_change(one: One, dummy_template: int, dummy_user: int, dummy_group: int):
    template_id = dummy_template
    user_id     = dummy_user
    group_id    = dummy_group
    user_and_group_change__test(one.template, template_id, user_id, group_id)




def test_template_user_and_group_not_changed(one: One, dummy_template: int):
    template_id = dummy_template
    user_and_group_not_changed__test(one.template, template_id)




def test_template_user_change(one: One, dummy_template: int, dummy_user: int):
    template_id = dummy_template
    user_id     = dummy_user
    user_change__test(one.template, template_id, user_id)




def test_template_group_change(one: One, dummy_template: int, dummy_group: int):
    template_id = dummy_template
    group_id    = dummy_group
    group_change__test(one.template, template_id, group_id)
