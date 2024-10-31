import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_brestadm_auth, run_command
from commands.image     import is_image_exist, delete_image, create_image_by_tempalte, change_image_user
from commands.user      import get_user_id_by_name

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

    delete_image(image_id)


@pytest.fixture
def prepare_image_datastore():
    template_file_path  = "/tmp/test_template_file"
    datastore_name      = "api_test_image_ds"
    datastore_template  = f"""
        NAME = {datastore_name}
        TYPE = IMAGE_DS
        DS_MAD = fs
        TM_MAD = shared
    """
    with open(template_file_path, "w") as template_file:
        template_file.write(datastore_template)

    datastore_id   = int(run_command(f"sudo onedatastore create {template_file_path} " + " | awk '{print $2}'"))
    
    
    yield datastore_id, datastore_name
    
    run_command(f"sudo onedatastore delete {datastore_id}")



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.clone(999999, "GregVetkin")


def test_datastore_not_exist(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneNoExistsException):
        one.image.clone(image_id, "GregVetkin", 999999)


def test_name_is_taken(prepare_image_datablock):
    one                  = One(BRESTADM_SESSION)
    image_id, image_name = prepare_image_datablock
    change_image_user(image_id, get_user_id_by_name("brestadm"))
    with pytest.raises(OneException):
        one.image.clone(image_id, image_name)


def test_only_image_datastore_support(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneActionException):
        one.image.clone(image_id, "GregVetkin", 2)


def test_clone_into_the_same_datastore(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    clone_id    = one.image.clone(image_id, "api_test_image_clone")
    assert is_image_exist(clone_id) == True
    delete_image(clone_id)


def test_clone_into_another_datastore(prepare_image_datastore, prepare_image_datablock):
    one             = One(BRESTADM_SESSION)
    image_id, _     = prepare_image_datablock
    datastore_id, _ = prepare_image_datastore
    clone_id        = one.image.clone(image_id, "api_test_image_clone", datastore_id)
    assert is_image_exist(clone_id) == True
    delete_image(clone_id)
