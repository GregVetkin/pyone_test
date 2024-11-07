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



def image_rights(image_id: int):
    rights = Image(image_id).info().PERMISSIONS

    return ((rights.OWNER.USE, rights.OWNER.MANAGE, rights.OWNER.ADMIN),
            (rights.GROUP.USE, rights.GROUP.MANAGE, rights.GROUP.ADMIN),
            (rights.OTHER.USE, rights.OTHER.MANAGE, rights.OTHER.ADMIN))
    


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.chmod(999999)



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("image", [DATABLOCK_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_change_image_rights(one: One, image: Image):
    image.chmod("000")
    image_id = image._id
    
    one.image.chmod(image_id, user_use=1)
    assert image_rights(image_id) == ((True, False, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image_id, user_manage=1)
    assert image_rights(image_id) == ((True, True, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image_id, user_admin=1)
    assert image_rights(image_id) == ((True, True, True), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image_id, user_admin=0)
    assert image_rights(image_id) == ((True, True, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image_id, user_manage=0)
    assert image_rights(image_id) == ((True, False, False), 
                                      (False, False, False), 
                                      (False, False, False))
    
    one.image.chmod(image_id, user_use=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))



    one.image.chmod(image_id, group_use=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (True, False, False), 
                                      (False, False, False))

    one.image.chmod(image_id, group_manage=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (True, True, False), 
                                      (False, False, False))

    one.image.chmod(image_id, group_admin=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (True, True, True), 
                                      (False, False, False))

    one.image.chmod(image_id, group_admin=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (True, True, False), 
                                      (False, False, False))

    one.image.chmod(image_id, group_manage=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (True, False, False), 
                                      (False, False, False))
    
    one.image.chmod(image_id, group_use=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))



    one.image.chmod(image_id, other_use=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, False, False))

    one.image.chmod(image_id, other_manage=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, False))

    one.image.chmod(image_id, other_admin=1)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, True))

    one.image.chmod(image_id, other_admin=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, False))

    one.image.chmod(image_id, other_manage=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, False, False))
    
    one.image.chmod(image_id, other_use=0)
    assert image_rights(image_id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))
