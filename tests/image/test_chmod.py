import pytest
from api                            import One
from config.tests                   import LOCK_LEVELS
from utils.other                    import wait_until
from tests._common_methods.chmod    import random_permissions__test
from tests._common_methods.chmod    import object_not_exist__test
from tests._common_methods.chmod    import chmod__test
from tests._common_methods.chmod    import cant_be_chmod__test



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    object_not_exist__test(one.image)




def test_chmod_image(one: One, dummy_image: int):
    image_id = dummy_image
    random_permissions__test(one.image, image_id)
    


@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_chmod_locked_image(one: One, dummy_image: int, lock_level: int):
    image_id = dummy_image

    one.image.lock(image_id, lock_level, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK.LOCKED == lock_level)

    if lock_level == 3:
        chmod__test(one.image, image_id, (0,0,-1,0,0,-1,0,0,-1))       # every 3rd param - is administration rights. -1 means to set as it was before (dont change)
    else:
        cant_be_chmod__test(one.image, image_id, (0,0,-1,0,0,-1,0,0,-1))
    
    cant_be_chmod__test(one.image, image_id, (1,1,1,1,1,1,1,1,1))

    one.image.unlock(image_id)
    wait_until(lambda: one.image.info(image_id, False).LOCK is None)