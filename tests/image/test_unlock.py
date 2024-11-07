import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image
from config             import BRESTADM


BRESTADM_AUTH     = get_user_auth(BRESTADM)
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
        one.image.unlock(99999)



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("lock_level", [0, 1, 2, 3, 4])
def test_unlock_image(one: One, image: Image, lock_level: int):
        if lock_level == 0:
            assert image.info().LOCK == None
        else:
            image.lock(lock_level)
            assert image.info().LOCK.LOCKED == lock_level

        one.image.unlock(image._id)
        assert image.info().LOCK == None


