import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_brestadm_auth, run_command
from commands.image     import get_image_type


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)


IMAGE_TYPES = ["OS", "CDROM", "DATABLOCK"]
FILE_TYPES  = ["KERNEL", "RAMDISK", "CONTEXT"]





@pytest.fixture
def prepare_image_for_image_ds():
    image_name  = "api_test_image"
    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))

    yield (image_id, image_name)

    run_command(f"sudo oneimage delete {image_id}")


@pytest.fixture
def prepare_image_for_file_ds():
    image_name = "api_test_file"
    file_path  = "/var/tmp/{file_name}"
    run_command(f"sudo dd if=/dev/urandom of={file_path} bs=1MiB count=10 status=none")
    image_id   = int(run_command(f"sudo oneimage create -d 2 --name {image_name} --type CONTEXT --path '{file_path}' " + " | awk '{print $2}'"))

    yield (image_id, image_name)

    run_command(f"sudo oneimage delete {image_id}")
    run_command(f"sudo rm -f {file_path}")



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.chtype(999999, "")


def test_incompatible_image_type_for_image_datastore(prepare_image_for_image_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_image_ds
    created_image_type  = get_image_type(image_id)

    for new_image_type in FILE_TYPES:
        with pytest.raises(OneActionException):
            one.image.chtype(image_id, new_image_type)

        current_image_type = get_image_type(image_id)
        assert current_image_type == created_image_type


def test_incompatible_file_type_for_file_datastore(prepare_image_for_file_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_file_ds
    created_image_type  = get_image_type(image_id)

    for new_image_type in IMAGE_TYPES:
        with pytest.raises(OneActionException):
            one.image.chtype(image_id, new_image_type)

        current_image_type = get_image_type(image_id)
        assert current_image_type == created_image_type


def test_available_image_types(prepare_image_for_image_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_image_ds

    for new_image_type in IMAGE_TYPES:
        one.image.chtype(image_id, new_image_type)
        current_image_type = get_image_type(image_id)
        assert current_image_type == new_image_type


def test_available_file_types(prepare_image_for_file_ds):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image_for_file_ds

    for new_image_type in FILE_TYPES:
        one.image.chtype(image_id, new_image_type)
        current_image_type = get_image_type(image_id)
        assert current_image_type == new_image_type


