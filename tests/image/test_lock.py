import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.image      import Image
from config             import BRESTADM



IMAGE_LOCK_LEVELS = [1, 2, 3, 4]
BRESTADM_AUTH = get_user_auth(BRESTADM)
STORAGE_IMAGE_TEMPLATE = """
NAME   = test_api_img_storage
TYPE   = IMAGE_DS
TM_MAD = ssh
DS_MAD = fs
"""
DATABLOCK_IMAGE_TEMPLATE = """
NAME = test_api_datablock
TYPE = DATABLOCK
SIZE = 1
"""

    

# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.lock(999999, lock_level=4)





@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", [0, 1, 2, 3, 4])
@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
def test_lock_image(one: One, image: Image, init_lock_lvl: int, lock_level: int, lock_check: bool):
    if init_lock_lvl == 0:
        assert image.info().LOCK == None
    else:
        image.lock(init_lock_lvl)
        assert image.info().LOCK.LOCKED == init_lock_lvl
    
    if lock_check and init_lock_lvl != 0:
        with pytest.raises(OneActionException):
            one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == init_lock_lvl
    else:
        one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == lock_level


