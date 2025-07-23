import pytest
import time
from api                import One
from pyone              import OneActionException, OneNoExistsException
from utils.other        import wait_until, get_unic_name
from utils.connection   import local_admin_ssh_conn
from utils.commands     import run_command_via_ssh



IMAGE_TYPES   = {0: "OS",
                 1: "CDROM",
                 2: "DATABLOCK"}
FILE_TYPES    = {3: "KERNEL",
                 4: "RAMDISK",
                 5: "CONTEXT"}




@pytest.fixture
def image_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template, -1)
    yield datastore_id
    one.datastore.delete(datastore_id)


@pytest.fixture(params=list(IMAGE_TYPES.values()))
def image_with_image_type(one: One, image_datastore: int, request):
    datastore_id = image_datastore
    image_type   = request.param
    file_path    = f"/var/tmp/{get_unic_name()}"
    run_command_via_ssh(local_admin_ssh_conn, f"dd if=/dev/urandom of={file_path} bs=1M count=1")
    time.sleep(1)
    template = f"""
        NAME = {get_unic_name()}
        TYPE = {image_type}
        PATH = {file_path}
    """
    image_id = one.image.allocate(template, datastore_id, False)
    yield image_id
    one.image.delete(image_id, True)
    wait_until(lambda: image_id not in [image.ID for image in one.imagepool.info().IMAGE])




@pytest.fixture
def file_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template, -1)
    yield datastore_id
    one.datastore.delete(datastore_id)



@pytest.fixture(params=list(FILE_TYPES.values()))
def image_with_file_type(one: One, file_datastore: int, request):
    datastore_id = file_datastore
    image_type   = request.param
    file_path    = f"/var/tmp/{get_unic_name()}"
    run_command_via_ssh(local_admin_ssh_conn, f"dd if=/dev/urandom of={file_path} bs=1M count=1")
    time.sleep(1)
    template = f"""
        NAME = {get_unic_name()}
        TYPE = {image_type}
        PATH = {file_path}
    """
    image_id = one.image.allocate(template, datastore_id, False)
    yield image_id
    one.image.delete(image_id, True)
    wait_until(lambda: image_id not in [image.ID for image in one.imagepool.info().IMAGE])



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    image_id = 99999
    new_type = "OS"
    with pytest.raises(OneNoExistsException):
        one.image.chtype(image_id, new_type)



@pytest.mark.parametrize("file_type", list(FILE_TYPES.values()))
def test_incompatible_type_for_image(one: One, image_with_image_type: int, file_type):
    image_id = image_with_image_type
    new_type = file_type
    image_type_before = one.image.info(image_id).TYPE
    with pytest.raises(OneActionException):
        one.image.chtype(image_id, new_type)
    image_type_after = one.image.info(image_id).TYPE
    assert image_type_before == image_type_after




@pytest.mark.parametrize("image_type", list(IMAGE_TYPES.values()))
def test_incompatible_type_for_file(one: One, image_with_file_type: int, image_type):
    image_id = image_with_file_type
    new_type = image_type
    image_type_before = one.image.info(image_id).TYPE
    with pytest.raises(OneActionException):
        one.image.chtype(image_id, new_type)
    image_type_after = one.image.info(image_id).TYPE
    assert image_type_before == image_type_after





@pytest.mark.parametrize("image_type", list(IMAGE_TYPES.values()))
def test_image_types(one: One, image_with_image_type: int, image_type):
    image_id = image_with_image_type
    new_type = image_type
    
    _id = one.image.chtype(image_id, new_type)
    assert _id == image_id
    assert one.image.info(image_id).TYPE == next((key for key, value in IMAGE_TYPES.items() if value == new_type))




@pytest.mark.parametrize("file_type", list(FILE_TYPES.values()))
def test_file_types(one: One, image_with_file_type: int, file_type):
    image_id = image_with_file_type
    new_type = file_type

    _id = one.image.chtype(image_id, new_type)

    assert _id == image_id
    assert one.image.info(image_id).TYPE == next((key for key, value in FILE_TYPES.items() if value == new_type))

