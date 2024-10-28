import pytest

from api    import One
from pyone  import OneServer, OneActionException, OneNoExistsException, OneException
from utils  import get_brestadm_auth, run_command


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)


IMAGE_TYPES = ["OS", "CDROM", "DATABLOCK"]
FILE_TYPES  = ["KERNEL", "RAMDISK", "CONTEXT"]

ERROR_INCOMPATIBLE_TYPE = "Cannot change image type to an incompatible type for the current datastore"


@pytest.fixture
def prepare_image():
    image_name  = "api_test_image"
    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))

    yield (image_id, image_name)

    run_command(f"sudo oneimage delete {image_id}")


@pytest.fixture
def prepare_file():
    file_name  = "api_test_file"
    file_path  = "/var/tmp/{file_name}"
    run_command(f"sudo dd if=/dev/urandom of={file_path} bs=1MiB count=10 status=none")
    file_id    = int(run_command(f"sudo oneimage create -d 2 --name {file_name} --type CONTEXT --path '{file_path}' " + " | awk '{print $2}'"))

    yield (file_id, file_name)

    run_command(f"sudo oneimage delete {file_id}")
    run_command(f"sudo rm -f {file_path}")



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException, match="Error getting image"):
        one.image.chtype(999999, "")



def test_incompatible_image_type_for_image_datastore(prepare_image):
    one                 = One(BRESTADM_SESSION)
    image_id, _         = prepare_image
    command_image_type  = f"sudo oneimage show {image_id} | grep TYPE | head -n 1 " + " | awk '{printf $3}'"
    created_image_type  = run_command(command_image_type)

    for new_image_type in FILE_TYPES:
        with pytest.raises(OneActionException, match=ERROR_INCOMPATIBLE_TYPE):
            one.image.chtype(image_id, new_image_type)
        image_type = run_command(command_image_type)
        assert image_type == created_image_type




def test_incompatible_file_type_for_file_datastore(prepare_file):
    one                 = One(BRESTADM_SESSION)
    file_id, _          = prepare_file
    command_file_type   = f"sudo oneimage show {file_id} | grep TYPE | head -n 1 " + " | awk '{printf $3}'"
    created_file_type   = run_command(command_file_type)

    for new_file_type in IMAGE_TYPES:
        with pytest.raises(OneActionException, match=ERROR_INCOMPATIBLE_TYPE):
            one.image.chtype(file_id, new_file_type)
        file_type = run_command(command_file_type)
        assert file_type == created_file_type





def test_available_image_types(prepare_image):
    pass



def test_available_file_types(prepare_file):
    pass


