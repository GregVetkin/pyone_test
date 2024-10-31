import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_brestadm_auth, run_command
from one_cli.image      import Image
from config             import API_URI, COMMAND_EXECUTOR


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image_user_group():
    image_name  = "api_test_image"
    user_name   = "api_test_user"
    group_name  = "api_test_group"

    image_id    = int(run_command(COMMAND_EXECUTOR + " " + f"oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    user_id     = int(run_command(COMMAND_EXECUTOR + " " + f"oneuser create {user_name} 12345678 " + " | awk '{print $2}'"))
    group_id    = int(run_command(COMMAND_EXECUTOR + " " + f"onegroup create {group_name} " + " | awk '{print $2}'"))

    yield ((image_id, image_name),
           (user_id, user_name),
           (group_id, group_name))

    run_command(COMMAND_EXECUTOR + " " + f"oneimage delete {image_id}")
    run_command(COMMAND_EXECUTOR + " " + f"oneuser delete {user_id}")
    run_command(COMMAND_EXECUTOR + " " + f"onegroup delete {group_id}")


# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist():
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.chown(999999)



def test_user_not_exist(prepare_image_user_group):
    (image_id, _), _, _ = prepare_image_user_group
    image_old_info      = Image(image_id).info()
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.chown(image_id, user_id=999999)
    image_new_info      = Image(image_id).info()

    assert image_old_info.UNAME == image_new_info.UNAME



def test_group_not_exist(prepare_image_user_group):
    (image_id, _), _, _ = prepare_image_user_group
    image_old_info      = Image(image_id).info()
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.chown(image_id, group_id=999999)
    image_new_info      = Image(image_id).info()

    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_and_group_change(prepare_image_user_group):
    (image_id, _), (user_id, user_name), (group_id, group_name) = prepare_image_user_group
    One(BRESTADM_SESSION).image.chown(image_id, user_id=user_id, group_id=group_id)
    image_new_info = Image(image_id).info()

    assert user_name  == image_new_info.UNAME
    assert group_name == image_new_info.GNAME



def test_image_user_and_group_not_changed(prepare_image_user_group):
    (image_id, _), _, _ = prepare_image_user_group
    image_old_info      = Image(image_id).info()
    One(BRESTADM_SESSION).image.chown(image_id)
    image_new_info      = Image(image_id).info()
    
    assert image_old_info.UNAME == image_new_info.UNAME
    assert image_old_info.GNAME == image_new_info.GNAME



def test_image_user_change(prepare_image_user_group):
    (image_id, _), (user_id, user_name), _ = prepare_image_user_group
    image_old_info = Image(image_id).info()
    One(BRESTADM_SESSION).image.chown(image_id, user_id=user_id)
    image_new_info = Image(image_id).info()

    assert image_new_info.UNAME == user_name
    assert image_new_info.GNAME == image_old_info.GNAME



def test_image_group_change(prepare_image_user_group):
    (image_id, _), _, (group_id, group_name)   = prepare_image_user_group
    image_old_info = Image(image_id).info()
    One(BRESTADM_SESSION).image.chown(image_id, group_id=group_id)
    image_new_info = Image(image_id).info()

    assert image_new_info.UNAME == image_old_info.UNAME
    assert image_new_info.GNAME == group_name

