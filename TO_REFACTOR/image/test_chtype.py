import pytest

from api                import One
from pyone              import OneActionException, OneNoExistsException
from utils              import create_temp_file, delete_temp_file, get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME


IMAGE_TYPES   = {0: "OS",
                 1: "CDROM",
                 2: "DATABLOCK"}
FILE_TYPES    = {3: "KERNEL",
                 4: "RAMDISK",
                 5: "CONTEXT"}


@pytest.fixture(scope="module")
def image_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture(scope="module")
def file_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def datablock_image(image_datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture
def context_image(file_datastore: Datastore):
    file_path       = "/var/tmp/test_file"
    image_template  = f"""
        NAME = {get_unic_name()}
        TYPE = CONTEXT
        PATH = {file_path}
    """
    create_temp_file(1, file_path)
    image_id = create_image(file_datastore._id, image_template)
    image    = Image(image_id)
    yield image
    image.delete()
    delete_temp_file(file_path)



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.chtype(999999, "VetkinType")



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
@pytest.mark.parametrize("file_type_id", list(FILE_TYPES.keys()))
def test_incompatible_type_for_image_datastore(one: One, datablock_image: Image, file_type_id):
    image_old_type = datablock_image.info().TYPE
    with pytest.raises(OneActionException):
        one.image.chtype(datablock_image._id, FILE_TYPES[file_type_id])
    image_new_type = datablock_image.info().TYPE
    assert image_old_type == image_new_type



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
@pytest.mark.parametrize("image_type_id", list(IMAGE_TYPES.keys()))
def test_incompatible_type_for_file_datastore(one: One, context_image: Image, image_type_id):
    image_old_type = context_image.info().TYPE
    with pytest.raises(OneActionException):
        one.image.chtype(context_image._id, IMAGE_TYPES[image_type_id])
    image_new_type = context_image.info().TYPE
    assert image_old_type == image_new_type



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
@pytest.mark.parametrize("image_type_id", list(IMAGE_TYPES.keys()))
def test_available_image_types(one: One, datablock_image: Image, image_type_id):
    one.image.chtype(datablock_image._id, IMAGE_TYPES[image_type_id])
    assert datablock_image.info().TYPE == image_type_id



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
@pytest.mark.parametrize("file_type_id", list(FILE_TYPES.keys()))
def test_available_file_types(one: One, context_image: Image, file_type_id):
    one.image.chtype(context_image._id, FILE_TYPES[file_type_id])
    assert context_image.info().TYPE == file_type_id

