import pytest

from api                import One
from config.tests       import LOCK_LEVELS
from utils.other        import wait_until

from tests._common_methods.update import update_and_merge__test
from tests._common_methods.update import update_and_replace__test
from tests._common_methods.update import update_if_not_exist__test
from tests._common_methods.update import cant_be_updated__test





# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    update_if_not_exist__test(one.image)



def test_update_by_replace(one: One, dummy_image: int):
    image_id = dummy_image
    update_and_replace__test(one.image, image_id)



def test_update_by_merge(one: One, dummy_image: int):
    image_id = dummy_image
    update_and_merge__test(one.image, image_id)




@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_update_locked_image(one: One, dummy_image: int, lock_level: int):
    image_id = dummy_image

    one.image.lock(image_id, lock_level, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK.LOCKED == lock_level)

    if lock_level == 3:
        update_and_replace__test(one.image, image_id)
        update_and_merge__test(one.image, image_id)
    else:
        cant_be_updated__test(one.image, image_id)

    one.image.lock(image_id, 0, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK is None)