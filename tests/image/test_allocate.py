import pytest

from api                import One
from pyone              import OneActionException, OneNoExistsException, OneException
from utils              import create_temp_file, delete_temp_file, get_unic_name
from one_cli.image      import Image, image_exist
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME





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
def system_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = system_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    with pytest.raises(OneNoExistsException):
        one.image.allocate(template, 999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_dont_check_capacity(one: One, image_datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1024000
    """
    image_id = one.image.allocate(template, image_datastore._id, False)
    image    = Image(image_id)
    assert image_exist(image_id)
    image.delete()



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_check_capacity(one: One, image_datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1024000
    """
    with pytest.raises(OneActionException):
        one.image.allocate(template, image_datastore._id, True)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_wrong_image_type_for_datastore(one: One, system_datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    with pytest.raises(OneException):
        one.image.allocate(template, system_datastore._id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_with_localfile_load(one: One, image_datastore: Datastore):
    file_path = "/tmp/testfile"
    create_temp_file(1, file_path)
    template  = f"""
        NAME = {get_unic_name()}
        TYPE = OS
        PATH = {file_path}
    """
    image_id = one.image.allocate(template, image_datastore._id)
    image    = Image(image_id)
    assert image_exist(image_id)
    image.delete()
    delete_temp_file(file_path)

