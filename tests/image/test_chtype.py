import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException
from utils              import get_brestadm_auth, run_command
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, COMMAND_EXECUTOR


BRESTADM_AUTH       = get_brestadm_auth()
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

    yield (image_id, image_name)

    Image(image_id).delete()


@pytest.fixture
def prepare_image_for_file_ds():
    image_name      = "api_test_file"
    file_path       = "/var/tmp/test_file"
    image_template  = f"""
        NAME = {image_name}
        TYPE = CONTEXT
        PATH = {file_path}
    """
    run_command(COMMAND_EXECUTOR + " " + f"dd if=/dev/urandom of={file_path} bs=1MiB count=10 status=none")
    image_id = create_image_by_tempalte(2, image_template)

    yield (image_id, image_name)

    Image(image_id).delete()
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {file_path}")



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    with pytest.raises(OneNoExistsException):
        One(BRESTADM_SESSION).image.chtype(999999, "")



def test_incompatible_image_type_for_image_datastore(prepare_image_for_image_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_image_ds
    created_image_type  = Image(image_id).info().TYPE

    for type_id in FILE_TYPES:
        with pytest.raises(OneActionException):
            one.image.chtype(image_id, FILE_TYPES[type_id])

        assert Image(image_id).info().TYPE == created_image_type



def test_incompatible_file_type_for_file_datastore(prepare_image_for_file_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_file_ds
    created_image_type  = Image(image_id).info().TYPE

    for type_id in IMAGE_TYPES:
        with pytest.raises(OneActionException):
            one.image.chtype(image_id, IMAGE_TYPES[type_id])
        assert Image(image_id).info().TYPE == created_image_type



def test_available_image_types(prepare_image_for_image_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_image_ds

    for type_id in IMAGE_TYPES:
        one.image.chtype(image_id, IMAGE_TYPES[type_id])
        assert Image(image_id).info().TYPE == type_id



def test_available_file_types(prepare_image_for_file_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_file_ds

    for type_id in FILE_TYPES:
        one.image.chtype(image_id, FILE_TYPES[type_id])
        assert Image(image_id).info().TYPE == type_id


