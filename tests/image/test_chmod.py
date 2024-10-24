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
        one.image.chmod(9999)


def test_change_image_rights():
    one         = One(BRESTADM_SESSION)
    image_name  = "test_change_image_rights"
    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))

    command_owner_rights = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep OWNER " + " | awk '{print $3}'"
    command_group_rights = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep GROUP " + " | awk '{print $3}'"
    command_other_rights = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep OTHER " + " | awk '{print $3}'"

    run_command(f"sudo oneimage chmod {image_id} 000")


    one.image.chmod(image_id, user_use=1)
    assert run_command(command_owner_rights) == "u--"

    one.image.chmod(image_id, user_manage=1)
    assert run_command(command_owner_rights) == "um-"

    one.image.chmod(image_id, user_admin=1)
    assert run_command(command_owner_rights) == "uma"

    one.image.chmod(image_id, user_admin=0)
    assert run_command(command_owner_rights) == "um-"

    one.image.chmod(image_id, user_manage=0)
    assert run_command(command_owner_rights) == "u--"
    
    one.image.chmod(image_id, user_use=0)
    assert run_command(command_owner_rights) == "---"



    one.image.chmod(image_id, group_use=1)
    assert run_command(command_group_rights) == "u--"

    one.image.chmod(image_id, group_manage=1)
    assert run_command(command_group_rights) == "um-"

    one.image.chmod(image_id, group_admin=1)
    assert run_command(command_group_rights) == "uma"

    one.image.chmod(image_id, group_admin=0)
    assert run_command(command_group_rights) == "um-"

    one.image.chmod(image_id, group_manage=0)
    assert run_command(command_group_rights) == "u--"
    
    one.image.chmod(image_id, group_use=0)
    assert run_command(command_group_rights) == "---"



    one.image.chmod(image_id, other_use=1)
    assert run_command(command_other_rights) == "u--"

    one.image.chmod(image_id, other_manage=1)
    assert run_command(command_other_rights) == "um-"

    one.image.chmod(image_id, other_admin=1)
    assert run_command(command_other_rights) == "uma"

    one.image.chmod(image_id, other_admin=0)
    assert run_command(command_other_rights) == "um-"

    one.image.chmod(image_id, other_manage=0)
    assert run_command(command_other_rights) == "u--"
    
    one.image.chmod(image_id, other_use=0)
    assert run_command(command_other_rights) == "---"

    
    run_command(f"sudo oneimage delete {image_name}")