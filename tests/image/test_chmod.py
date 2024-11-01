import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)




@pytest.fixture
def prepare_datablock_with_000_rights():
    image_template = """
        NAME = test_api_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template)
    image    = Image(image_id)

    image.chmod("000")
    yield image
    image.delete()


def image_rights(image_id: int):
    rights = Image(image_id).info().PERMISSIONS

    return ((rights.OWNER.USE, rights.OWNER.MANAGE, rights.OWNER.ADMIN),
            (rights.GROUP.USE, rights.GROUP.MANAGE, rights.GROUP.ADMIN),
            (rights.OTHER.USE, rights.OTHER.MANAGE, rights.OTHER.ADMIN))
    


# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chmod(999999)



def test_change_image_rights(prepare_datablock_with_000_rights):
    one      = One(BRESTADM_SESSION)
    image    = prepare_datablock_with_000_rights
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
