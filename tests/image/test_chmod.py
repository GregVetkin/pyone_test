import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    image_template = """
        NAME = test_api_image
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(datastore._id, image_template)
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


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.chmod(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_image_rights(one: One, image: Datastore):
    one.image.chmod(image._id, user_use=1)
    assert image_rights(image._id) == ((True, False, False), 
                                      (False, False, False), 
                                      (False, False, False))
    
    one.image.chmod(image._id, user_manage=1)
    assert image_rights(image._id) == ((True, True, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, user_admin=1)
    assert image_rights(image._id) == ((True, True, True), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, user_admin=0)
    assert image_rights(image._id) == ((True, True, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, user_manage=0)
    assert image_rights(image._id) == ((True, False, False), 
                                      (False, False, False), 
                                      (False, False, False))
    
    one.image.chmod(image._id, user_use=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, group_use=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (True, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, group_manage=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (True, True, False), 
                                      (False, False, False))

    one.image.chmod(image._id, group_admin=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (True, True, True), 
                                      (False, False, False))

    one.image.chmod(image._id, group_admin=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (True, True, False), 
                                      (False, False, False))

    one.image.chmod(image._id, group_manage=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (True, False, False), 
                                      (False, False, False))
    
    one.image.chmod(image._id, group_use=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))

    one.image.chmod(image._id, other_use=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, False, False))

    one.image.chmod(image._id, other_manage=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, False))

    one.image.chmod(image._id, other_admin=1)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, True))

    one.image.chmod(image._id, other_admin=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, True, False))

    one.image.chmod(image._id, other_manage=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (True, False, False))
    
    one.image.chmod(image._id, other_use=0)
    assert image_rights(image._id) == ((False, False, False), 
                                      (False, False, False), 
                                      (False, False, False))
