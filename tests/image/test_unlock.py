import pytest

from api                            import One
from utils.other                    import wait_until
from config.tests                   import LOCK_LEVELS

from tests._common_methods.unlock   import unlock__test
from tests._common_methods.unlock   import unlock_if_not_exist__test




@pytest.fixture(params=LOCK_LEVELS)
def locked_image(one: One, dummy_image: int, request):
    image_id    = dummy_image
    lock_level  = request.param

    one.image.lock(image_id, lock_level, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK.LOCKED == lock_level)

    yield image_id

    one.image.unlock(image_id)
    wait_until(lambda: one.image.info(image_id, False).LOCK is None)


# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    unlock_if_not_exist__test(one.image)


def test_unlocked_image(one: One, dummy_image: int):
    image_id = dummy_image
    unlock__test(one.image, image_id)


def test_locked_image(one: One, locked_image: int):
    image_id = locked_image
    
    assert one.image.info(image_id).LOCK is not None
    unlock__test(one.image, image_id)

