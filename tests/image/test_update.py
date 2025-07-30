import pytest
import pyone

from api                import One
from config.tests       import LOCK_LEVELS
from utils.other        import wait_until

from tests._common_methods.update import update__test, not_exist__test






# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    not_exist__test(one.image)




@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_image: int, update_type: int):
    image_id = dummy_image
    update__test(one.image, image_id, update_type)





@pytest.mark.parametrize("update_type", [0, 1])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_update_locked_image(one: One, dummy_image: int, update_type: int, lock_level: int):
    image_id = dummy_image

    one.image.lock(image_id, lock_level, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK is not None)

    if lock_level == 3:
        update__test(one.image, image_id, update_type)
    else:
        with pytest.raises(pyone.OneException):
            update__test(one.image, image_id, update_type)

    one.image.unlock(image_id)
    wait_until(lambda: one.image.info(image_id, False).LOCK is None)