import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_brestadm_auth, run_command
from commands.image     import get_image_user_rights, get_image_group_rights, get_image_other_rights

from config             import API_URI


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)




@pytest.fixture
def prepare_datablock_with_000_rights():
    image_name  = "test_change_image_rights"
    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    run_command(f"sudo oneimage chmod {image_id} 000")
    yield   image_id, image_name
    run_command(f"sudo oneimage delete {image_name}")



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chmod(999999)


def test_change_image_rights(prepare_datablock_with_000_rights):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_datablock_with_000_rights
    
    
    one.image.chmod(image_id, user_use=1)
    assert get_image_user_rights(image_id) == "u--"

    one.image.chmod(image_id, user_manage=1)
    assert get_image_user_rights(image_id) == "um-"

    one.image.chmod(image_id, user_admin=1)
    assert get_image_user_rights(image_id) == "uma"

    one.image.chmod(image_id, user_admin=0)
    assert get_image_user_rights(image_id) == "um-"

    one.image.chmod(image_id, user_manage=0)
    assert get_image_user_rights(image_id) == "u--"
    
    one.image.chmod(image_id, user_use=0)
    assert get_image_user_rights(image_id) == "---"



    one.image.chmod(image_id, group_use=1)
    assert get_image_group_rights(image_id) == "u--"

    one.image.chmod(image_id, group_manage=1)
    assert get_image_group_rights(image_id) == "um-"

    one.image.chmod(image_id, group_admin=1)
    assert get_image_group_rights(image_id) == "uma"

    one.image.chmod(image_id, group_admin=0)
    assert get_image_group_rights(image_id) == "um-"

    one.image.chmod(image_id, group_manage=0)
    assert get_image_group_rights(image_id) == "u--"
    
    one.image.chmod(image_id, group_use=0)
    assert get_image_group_rights(image_id) == "---"



    one.image.chmod(image_id, other_use=1)
    assert get_image_other_rights(image_id) == "u--"

    one.image.chmod(image_id, other_manage=1)
    assert get_image_other_rights(image_id) == "um-"

    one.image.chmod(image_id, other_admin=1)
    assert get_image_other_rights(image_id) == "uma"

    one.image.chmod(image_id, other_admin=0)
    assert get_image_other_rights(image_id) == "um-"

    one.image.chmod(image_id, other_manage=0)
    assert get_image_other_rights(image_id) == "u--"
    
    one.image.chmod(image_id, other_use=0)
    assert get_image_other_rights(image_id) == "---"
