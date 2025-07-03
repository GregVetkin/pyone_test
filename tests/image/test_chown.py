import pytest
from api       import One

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




def test_image_not_exist(one: One):
    object_not_exist__test(one.image)


def test_user_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    user_not_exist__test(one.image, image_id)


def test_group_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    group_not_exist__test(one.image, image_id)




def test_user_and_group_change(one: One, dummy_image: int, dummy_user: int, dummy_group: int):
    image_id = dummy_image
    user_id  = dummy_user
    group_id = dummy_group
    user_and_group_change__test(one.image, image_id, user_id, group_id)



def test_user_and_group_not_changed(one: One, dummy_image: int):
    image_id = dummy_image
    user_and_group_not_changed__test(one.image, image_id)




def test_user_change(one: One, dummy_image: int, dummy_user: int):
    image_id = dummy_image
    user_id  = dummy_user
    user_change__test(one.image, image_id, user_id)


def test_group_change(one: One, dummy_image: int, dummy_group: int):
    image_id = dummy_image
    group_id = dummy_group
    group_change__test(one.image, image_id, group_id)
