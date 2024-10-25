import pytest

from api    import One
from pyone  import OneServer, OneActionException, OneNoExistsException, OneException
from utils  import get_brestadm_auth, run_command


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)




@pytest.fixture
def prepare_image_user_group():
    image_name  = "api_test_image"
    user_name   = "api_test_user"
    group_name  = "api_test_group"

    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    user_id     = int(run_command(f"sudo oneuser create {user_name} 12345678 " + " | awk '{print $2}'"))
    group_id    = int(run_command(f"sudo onegroup create {group_name} " + " | awk '{print $2}'"))

    yield ((image_id, image_name),
           (user_id, user_name),
           (group_id, group_name))

    run_command(f"sudo oneimage delete {image_id}")
    run_command(f"sudo oneuser delete {user_id}")
    run_command(f"sudo onegroup delete {group_id}")



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException, match="Error getting image"):
        one.image.chown(999999)



def test_user_not_exist(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, _, _    = prepare_image_user_group
    image_id, _         = image_data
    command_image_user  = f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'"

    image_user      = run_command(command_image_user)

    with pytest.raises(OneNoExistsException, match="Error getting user"):
        one.image.chown(image_id, user_id=999999)

    new_image_user  = run_command(command_image_user)

    assert image_user == new_image_user



def test_group_not_exist(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, _, _    = prepare_image_user_group
    image_id, _         = image_data
    command_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"


    image_group     = run_command(command_image_group)

    with pytest.raises(OneNoExistsException, match="Error getting group"):
        one.image.chown(image_id, group_id=999999)

    new_image_group = run_command(command_image_group)

    assert image_group == new_image_group



def test_image_user_and_group_change(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, user_data, group_data       = prepare_image_user_group
    image_id, _                             = image_data
    created_user_id, created_user_name      = user_data
    created_group_id, created_group_name    = group_data

    command_image_user  = f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'"
    command_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"

    one.image.chown(image_id, user_id=created_user_id, group_id=created_group_id)

    image_user_name     = run_command(command_image_user)
    image_group_name    = run_command(command_image_group)

    assert image_user_name   == created_user_name
    assert image_group_name  == created_group_name



def test_image_user_and_group_not_changed(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, _, _    = prepare_image_user_group
    image_id, _         = image_data

    command_image_user  = f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'"
    command_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"

    image_user          = run_command(command_image_user)
    image_group         = run_command(command_image_group)

    one.image.chown(image_id)

    new_image_user      = run_command(command_image_user)
    new_image_group     = run_command(command_image_group)
    

    assert image_user   == new_image_user
    assert image_group  == new_image_group



def test_image_user_change(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, user_data, _            = prepare_image_user_group
    image_id, _                         = image_data
    created_user_id, created_user_name  = user_data

    command_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"
    command_image_user  = f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'"

    image_group     = run_command(command_image_group)

    one.image.chown(image_id, user_id=created_user_id)

    new_image_user  = run_command(command_image_user)
    new_image_group = run_command(command_image_group)

    assert new_image_user   == created_user_name
    assert new_image_group  == image_group



def test_image_group_change(prepare_image_user_group):
    one = One(BRESTADM_SESSION)

    image_data, _, group_data               = prepare_image_user_group
    image_id, _                             = image_data
    created_group_id, created_group_name    = group_data


    command_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"
    command_image_user  = f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'"


    image_user      = run_command(command_image_user)

    one.image.chown(image_id, group_id=created_group_id)

    new_image_user  = run_command(command_image_user)
    new_image_group = run_command(command_image_group)

    assert new_image_user   == image_user
    assert new_image_group  == created_group_name


