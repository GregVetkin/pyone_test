import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_user_auth, run_command
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, COMMAND_EXECUTOR, BRESTADM


BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
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
def prepare_user():
    user_name   = "api_test_user"
    user_id     = int(run_command(COMMAND_EXECUTOR + " " + f"oneuser create {user_name} 12345678 " + " | awk '{print $2}'"))
    yield (user_id, user_name)
    run_command(COMMAND_EXECUTOR + " " + f"oneuser delete {user_id}")



@pytest.fixture
def prepare_group():
    group_name  = "api_test_group"
    group_id    = int(run_command(COMMAND_EXECUTOR + " " + f"onegroup create {group_name} " + " | awk '{print $2}'"))
    yield (group_id, group_name)
    run_command(COMMAND_EXECUTOR + " " + f"onegroup delete {group_id}")


# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chown(999999)



def test_user_not_exist(prepare_image):
    image           = prepare_image
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, user_id=999999)

    image_new_info  = image.info()

    assert image_old_info.UNAME == image_new_info.UNAME



def test_group_not_exist(prepare_image):
    image           = prepare_image
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, group_id=999999)

    image_new_info  = image.info()

    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_and_group_change(prepare_image, prepare_user, prepare_group):
    image                   = prepare_image
    user_id, user_name      = prepare_user
    group_id, group_name    = prepare_group
    
    one = One(BRESTADM_SESSION)

    one.image.chown(image._id, user_id=user_id, group_id=group_id)
    image_new_info = image.info()

    assert user_name  == image_new_info.UNAME
    assert group_name == image_new_info.GNAME



def test_image_user_and_group_not_changed(prepare_image):
    image           = prepare_image
    image_old_info  = image.info()
    one             = One(BRESTADM_SESSION)

    one.image.chown(image._id)
    image_new_info  = image.info()
    
    assert image_old_info.UNAME == image_new_info.UNAME
    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_change(prepare_image, prepare_user):
    image               = prepare_image
    user_id, user_name  = prepare_user
    image_old_info      = image.info()
    one                 = One(BRESTADM_SESSION)

    one.image.chown(image._id, user_id=user_id)
    image_new_info  = image.info()

    assert image_new_info.UNAME == user_name
    assert image_new_info.GNAME == image_old_info.GNAME



def test_image_group_change(prepare_image, prepare_group):
    image                   = prepare_image
    group_id, group_name    = prepare_group
    image_old_info          = image.info()
    one                     = One(BRESTADM_SESSION)

    one.image.chown(image._id, group_id=group_id)
    image_new_info  = image.info()

    assert image_new_info.UNAME == image_old_info.UNAME
    assert image_new_info.GNAME == group_name

