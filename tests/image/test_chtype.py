import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException
from utils              import get_user_auth, create_temp_file, delete_temp_file
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)
IMAGE_TYPES         = {0: "OS",
                       1: "CDROM",
                       2: "DATABLOCK"}
FILE_TYPES          = {3: "KERNEL",
                       4: "RAMDISK",
                       5: "CONTEXT"}





@pytest.fixture
def prepare_image_for_image_ds():
    image_name      = "api_test_image"
    image_template  = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template)
    image    = Image(image_id)

    yield image

    image.delete()



@pytest.fixture
def prepare_image_for_file_ds():
    file_path       = "/var/tmp/test_file"
    image_template  = f"""
        NAME = api_test_file
        TYPE = CONTEXT
        PATH = {file_path}
    """
    create_temp_file(10, file_path)
    image_id = create_image_by_tempalte(2, image_template)
    image    = Image(image_id)

    yield image

    image.delete()
    delete_temp_file(file_path)



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chtype(999999, "")



@pytest.mark.parametrize("file_type_id", list(FILE_TYPES.keys()))
def test_incompatible_image_type_for_image_datastore(prepare_image_for_image_ds, file_type_id):
    one        = One(BRESTADM_SESSION)
    image      = prepare_image_for_image_ds
    image_info = image.info()
    image_type = image_info.TYPE

    with pytest.raises(OneActionException):
        one.image.chtype(image._id, FILE_TYPES[file_type_id])
    assert image.info().TYPE == image_type



@pytest.mark.parametrize("image_type_id", list(IMAGE_TYPES.keys()))
def test_incompatible_file_type_for_file_datastore(prepare_image_for_file_ds, image_type_id):
    one        = One(BRESTADM_SESSION)
    image      = prepare_image_for_file_ds
    image_info = image.info()
    image_type = image_info.TYPE

    with pytest.raises(OneActionException):
        one.image.chtype(image._id, IMAGE_TYPES[image_type_id])
    assert image.info().TYPE == image_type



@pytest.mark.parametrize("image_type_id", list(IMAGE_TYPES.keys()))
def test_available_image_types(prepare_image_for_image_ds, image_type_id):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_for_image_ds
    one.image.chtype(image._id, IMAGE_TYPES[image_type_id])
    assert image.info().TYPE == image_type_id



@pytest.mark.parametrize("file_type_id", list(FILE_TYPES.keys()))
def test_available_file_types(prepare_image_for_file_ds, file_type_id):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_for_file_ds
    one.image.chtype(image._id, FILE_TYPES[file_type_id])
    assert image.info().TYPE == file_type_id


