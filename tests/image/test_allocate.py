import pytest

from api                import One
from pyone              import OneActionException, OneNoExistsException, OneException
from utils              import get_user_auth, create_temp_file, delete_temp_file
from one_cli.image      import Image, image_exist
from one_cli.datastore  import Datastore
from config             import BRESTADM



BRESTADM_AUTH          = get_user_auth(BRESTADM)
STORAGE_IMAGE_TEMPLATE = """
NAME   = test_api_img_storage
TYPE   = IMAGE_DS
TM_MAD = ssh
DS_MAD = fs
"""
STORAGE_SYSTEM_TEMPLATE = """
NAME   = test_api_sys_storage
TYPE   = SYSTEM_DS
TM_MAD = ssh
"""




# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
@pytest.mark.parametrize("cap_check", [True, False])
def test_capacity_check(one: One, datastore: Datastore, cap_check: bool):
    template = """
        NAME = api_test_image_1
        TYPE = DATABLOCK
        SIZE = 1024000
    """
    if cap_check:
        with pytest.raises(OneActionException):
            one.image.allocate(template, datastore._id, cap_check)
    else:
        image_id  = one.image.allocate(template, datastore._id, cap_check)
        image     = Image(image_id)
        assert image_exist(image_id) == True
        image.delete()



@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_datastore_not_exist(one: One):
    template = """
        NAME = api_test_image_3
        TYPE = DATABLOCK
        SIZE = 1 
    """
    with pytest.raises(OneNoExistsException):
        one.image.allocate(template, 99999)



@pytest.mark.parametrize("datastore", [STORAGE_SYSTEM_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_wrong_datastore(one: One, datastore: Datastore):
    template = """
        NAME = api_test_image_4
        TYPE = DATABLOCK
        SIZE = 1
    """
    with pytest.raises(OneException):
        one.image.allocate(template, datastore._id)



@pytest.mark.parametrize("datastore", [STORAGE_IMAGE_TEMPLATE,], indirect=True)
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_local_file_load(one: One, datastore: Datastore):
    file_path = "/tmp/testfile"
    create_temp_file(1, file_path)
    template  = f"""
        NAME = api_test_image_6
        TYPE = OS
        PATH = {file_path}
    """
    image_id = one.image.allocate(template, datastore._id)
    image    = Image(image_id)
    assert image_exist(image_id) == True
    image.delete()
    delete_temp_file(file_path)
