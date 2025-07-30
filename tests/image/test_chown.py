import pyone
import pytest
import random

from api                            import One
from tests._common_methods.chown    import not_exist__test, chown__test





# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    not_exist__test(one.image)


def test_user_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    user_id  = random.randint(9999, 999999)
    group_id = -1

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.image, image_id, user_id, group_id)



def test_group_not_exist(one: One, dummy_image: int):
    image_id = dummy_image
    user_id  = -1
    group_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.image, image_id, user_id, group_id)




def test_user_and_group_change(one: One, dummy_image: int, dummy_user: int, dummy_group: int):
    image_id = dummy_image
    user_id  = dummy_user
    group_id = dummy_group

    chown__test(one.image, image_id, user_id, group_id)



def test_user_and_group_not_changed(one: One, dummy_image: int):
    image_id = dummy_image
    user_id  = -1
    group_id = -1

    chown__test(one.image, image_id, user_id, group_id)




def test_only_user_change(one: One, dummy_image: int, dummy_user: int):
    image_id = dummy_image
    user_id  = dummy_user
    group_id = -1

    chown__test(one.image, image_id, user_id, group_id)


def test_only_group_change(one: One, dummy_image: int, dummy_group: int):
    image_id = dummy_image
    user_id  = -1
    group_id = dummy_group
    chown__test(one.image, image_id, user_id, group_id)
