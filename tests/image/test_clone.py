import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_brestadm_auth
from commands.user      import get_user_id_by_name
from one_cli.image      import create_image_by_tempalte, Image
from one_cli.datastore  import create_ds_by_tempalte, Datastore
from config             import API_URI


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image_datablock():
    image_name      = "api_test_image"
    image_template  = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield (image_id, image_name)

    Image(image_id).delete()


@pytest.fixture
def prepare_image_datastore():
    datastore_template = """
        NAME = api_test_image_ds
        TYPE = IMAGE_DS
        DS_MAD = fs
        TM_MAD = shared
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    
    yield datastore_id
    
    Datastore(datastore_id).delete()



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.clone(999999, "GregVetkin")



def test_datastore_not_exist(prepare_image_datablock):
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.clone(image_id, "GregVetkin", 999999)



def test_name_is_taken(prepare_image_datablock):
    image_id, image_name = prepare_image_datablock
    Image(image_id).chown(get_user_id_by_name("brestadm"))
    with pytest.raises(OneException):
        One(BRESTADM_SESSION).image.clone(image_id, image_name)



def test_only_image_datastore_support(prepare_image_datablock):
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneActionException):
        One(BRESTADM_SESSION).image.clone(image_id, "GregVetkin", 2)



def test_clone_into_the_same_datastore(prepare_image_datablock):
    image_id, _ = prepare_image_datablock
    clone_id    = One(BRESTADM_SESSION).image.clone(image_id, "api_test_image_clone")
    clone       = Image(clone_id)
    image       = Image(image_id)

    assert clone.info().DATASTORE_ID == image.info().DATASTORE_ID
    
    clone.delete()



def test_clone_into_another_datastore(prepare_image_datastore, prepare_image_datablock):
    image_id, _     = prepare_image_datablock
    datastore_id    = prepare_image_datastore
    clone_id        = One(BRESTADM_SESSION).image.clone(image_id, "api_test_image_clone", datastore_id)
    clone           = Image(clone_id)

    assert clone.info().DATASTORE_ID == datastore_id

    clone.delete()
