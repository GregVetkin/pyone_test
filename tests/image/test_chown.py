import pytest

from api    import One
from pyone  import OneServer, OneActionException, OneNoExistsException, OneException
from utils  import get_brestadm_auth, run_command


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)





def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException, match="Error getting image"):
        one.image.chown(999999)



def test_user_not_exist():
    one = One(BRESTADM_SESSION)

    image_name              = "test_user_not_exist"
    image_id                = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    command_get_image_user  = f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'"
    image_user              = run_command(command_get_image_user)

    with pytest.raises(OneNoExistsException, match="Error getting user"):
        one.image.chown(image_id, user_id=999999)

    assert image_user == run_command(command_get_image_user)

    run_command(f"sudo oneimage delete {image_name}")



def test_group_not_exist():
    one = One(BRESTADM_SESSION)

    image_name              = "test_group_not_exist"
    image_id                = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    command_get_image_group = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"
    image_group             = run_command(command_get_image_group)

    with pytest.raises(OneNoExistsException, match="Error getting group"):
        one.image.chown(image_id, group_id=999999)

    assert image_group == run_command(command_get_image_group)

    run_command(f"sudo oneimage delete {image_name}")



def test_image_user_and_group_change():
    one = One(BRESTADM_SESSION)

    new_user_name   = "api_test_user"
    new_group_name  = "api_test_group"
    image_name      = "test_image_user_and_group_change"

    image_id        = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    new_user_id     = int(run_command(f"sudo oneuser create {new_user_name} 12345678 " + " | awk '{print $2}'"))
    new_group_id    = int(run_command(f"sudo onegroup create {new_group_name} " + " | awk '{print $2}'"))


    one.image.chown(image_id, user_id=new_user_id, group_id=new_group_id)

    image_user      = run_command(f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'")
    image_group     = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")


    assert image_user   == new_user_name
    assert image_group  == new_group_name

    run_command(f"sudo oneimage delete {image_name}")
    run_command(f"sudo oneuser delete {new_user_name}")
    run_command(f"sudo onegroup delete {new_group_name}")



def test_image_user_and_group_not_changed():
    one = One(BRESTADM_SESSION)

    image_name          = "test_image_user_and_group_not_changed"
    
    image_id            = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    image_user          = run_command(f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'")
    image_group         = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")

    one.image.chown(image_id)

    new_image_user       = run_command(f"sudo oneimage show {image_id} | grep USER " + " | awk '{print $3}'")
    new_image_group      = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")
    

    assert image_user   == new_image_user
    assert image_group  == new_image_group

    run_command(f"sudo oneimage delete {image_name}")



def test_image_user_change():
    one = One(BRESTADM_SESSION)

    new_user_name   = "api_test_user"
    image_name      = "test_image_user_change"

    image_id        = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    new_user_id     = int(run_command(f"sudo oneuser create {new_user_name} 12345678 " + " | awk '{print $2}'"))
    image_group     = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")

    one.image.chown(image_id, user_id=new_user_id)

    new_image_user  = run_command(f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'")
    new_image_group = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")

    assert new_image_user   == new_user_name
    assert new_image_group  == image_group

    run_command(f"sudo oneimage delete {image_name}")
    run_command(f"sudo oneuser delete {new_user_name}")



def test_image_group_change():
    one = One(BRESTADM_SESSION)

    new_group_name  = "api_group_user"
    image_name      = "test_image_group_change"

    image_id        = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    new_group_id    = int(run_command(f"sudo onegroup create {new_group_name} " + " | awk '{print $2}'"))
    image_user      = run_command(f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'")

    one.image.chown(image_id, group_id=new_group_id)

    new_image_user  = run_command(f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'")
    new_image_group = run_command(f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'")

    assert new_image_user   == image_user
    assert new_image_group  == new_group_name

    run_command(f"sudo oneimage delete {image_name}")
    run_command(f"sudo onegroup delete {new_group_name}")