import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_user_auth
from commands.user      import get_user_id_by_name
from one_cli.image      import create_image_by_tempalte, Image
from one_cli.datastore  import create_ds_by_tempalte, Datastore
from config             import API_URI, BRESTADM


BRESTADM_AUTH    = get_user_auth(BRESTADM)
BRESTADM_SESSION = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image_datablock():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)
    
    yield image

    image.delete()


@pytest.fixture
def prepare_image_datastore():
    datastore_template = """
        NAME = api_test_image_ds
        TYPE = IMAGE_DS
        DS_MAD = fs
        TM_MAD = shared
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)

    yield datastore
    
    datastore.delete()



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.clone(999999, "GregVetkin")



def test_datastore_not_exist(prepare_image_datablock):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_datablock

    with pytest.raises(OneNoExistsException):
        one.image.clone(image._id, "GregVetkin", 999999)



def test_name_is_taken(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image_datablock
    image_info  = image.info()
    brestadm_id = get_user_id_by_name("brestadm")
    
    if image.info().UID != brestadm_id:
        image.chown(brestadm_id)

    with pytest.raises(OneException):
        one.image.clone(image._id, image_info.NAME)



def test_only_image_datastore_support(prepare_image_datablock):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_datablock

    with pytest.raises(OneActionException):
        one.image.clone(image._id, "GregVetkin", 2)



def test_clone_into_the_same_datastore(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image_datablock
    clone_id    = one.image.clone(image._id, "api_test_image_clone")
    clone       = Image(clone_id)

    assert clone.info().DATASTORE_ID == image.info().DATASTORE_ID
    
    clone.delete()



def test_clone_into_another_datastore(prepare_image_datastore, prepare_image_datablock):
    one       = One(BRESTADM_SESSION)
    image     = prepare_image_datablock
    datastore = prepare_image_datastore
    clone_id  = one.image.clone(image._id, "api_test_image_clone_", datastore._id)
    clone     = Image(clone_id)

    assert clone.info().DATASTORE_ID == datastore._id

    clone.delete()
