import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image
from one_cli.user       import User
from one_cli.group      import Group
from config             import BRESTADM


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
        one.image.chown(999999)



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_user_not_exist(one: One, image: Image):
    image_old_info = image.info()
    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, user_id=999999)
    image_new_info = image.info()

    assert image_old_info.UNAME == image_new_info.UNAME



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_group_not_exist(one: One, image: Image):
    image_old_info = image.info()
    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, group_id=999999)
    image_new_info = image.info()

    assert image_old_info.GNAME == image_new_info.GNAME



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("user", ["test_api_user",], indirect=True)
@pytest.mark.parametrize("group", ["test_api_group",], indirect=True)
def test_user_and_group_change(one: One, image: Image, user: User, group: Group):
    one.image.chown(image._id, user_id=user._id, group_id=group._id)
    image_new_info = image.info()

    assert user._id  == image_new_info.UID
    assert group._id == image_new_info.GID




@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_image_user_and_group_not_changed(one: One, image: Image):
    image_old_info = image.info()
    one.image.chown(image._id)
    image_new_info = image.info()
    
    assert image_old_info.UNAME == image_new_info.UNAME
    assert image_old_info.GNAME == image_new_info.GNAME



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("user", ["test_api_user",], indirect=True)
def test_image_user_change(one: One, image: Image, user: User):
    image_old_info = image.info()
    one.image.chown(image._id, user_id=user._id)
    image_new_info = image.info()

    assert image_new_info.UID == user._id
    assert image_new_info.GID == image_old_info.GID




@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("group", ["test_api_group",], indirect=True)
def test_image_group_change(one: One, image: Image, group: Group):
    image_old_info = image.info()
    one.image.chown(image._id, group_id=group._id)
    image_new_info = image.info()

    assert image_new_info.UID == image_old_info.UID
    assert image_new_info.GID == group._id

