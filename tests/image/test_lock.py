import pytest

from api                import One
from utils.other        import wait_until
from config.tests       import LOCK_LEVELS

from tests._common_methods.lock import lock_if_not_exist__test
from tests._common_methods.lock import lock_unlocked__test
from tests._common_methods.lock import lock_locked__test




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
    lock_if_not_exist__test(one.image)


@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_unlocked_image(one: One, dummy_image: int, lock_level: int, lock_check: bool):
    image_id = dummy_image
    lock_unlocked__test(one.image, image_id, lock_level, lock_check)

    one.image.unlock(image_id)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_locked_image(one: One, locked_image: int, lock_level: int, lock_check: bool):
    image_id = locked_image

    assert one.image.info(image_id).LOCK is not None
    lock_locked__test(one.image, image_id, lock_level, lock_check)

    one.image.unlock(image_id)