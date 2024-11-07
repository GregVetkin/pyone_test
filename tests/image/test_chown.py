import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import API_URI, BRESTADM


BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def image():
    template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, template)
    image    = Image(image_id)
    yield image
    image.delete()
    
    

@pytest.fixture
def user():
    user_id = create_user("api_test_user")
    user    = User(user_id)
    yield user
    user.delete()



@pytest.fixture
def group():
    group_id = create_group("api_test_group")
    group    = Group(group_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chown(999999)



def test_user_not_exist(image: Image):
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, user_id=999999)

    image_new_info  = image.info()

    assert image_old_info.UNAME == image_new_info.UNAME



def test_group_not_exist(image: Image):
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, group_id=999999)

    image_new_info  = image.info()

    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_and_group_change(image: Image, user: User, group: Group):

    one = One(BRESTADM_SESSION)

    one.image.chown(image._id, user._id, group._id)
    image_new_info = image.info()

    assert user._id  == image_new_info.UID
    assert group._id == image_new_info.GID



def test_image_user_and_group_not_changed(image: Image):
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    one.image.chown(image._id)
    image_new_info  = image.info()
    
    assert image_old_info.UNAME == image_new_info.UNAME
    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_change(image: Image, user: User):
    image_old_info      = image.info()
    one                 = One(BRESTADM_SESSION)

    one.image.chown(image._id, user_id=user._id)
    image_new_info  = image.info()

    assert image_new_info.UID   == user._id
    assert image_new_info.GID == image_old_info.GID



def test_image_group_change(image: Image, group: Group):
    image_old_info          = image.info()
    one                     = One(BRESTADM_SESSION)

    one.image.chown(image._id, group_id=group._id)
    image_new_info  = image.info()

    assert image_new_info.UID == image_old_info.UID
    assert image_new_info.GID   == group._id

