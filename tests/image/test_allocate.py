import pytest

from api            import One
from pyone          import OneServer, OneActionException, OneNoExistsException, OneException
from utils          import get_user_auth, run_command
from one_cli.image  import Image, image_exist
from config         import API_URI, COMMAND_EXECUTOR, BRESTADM



BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)




# =================================================================================================
# TESTS
# =================================================================================================


def test_create_datablock_and_dont_check_capacity():
    template = """
        NAME = api_test_image_1
        TYPE = DATABLOCK
        SIZE = 1024000
    """
    one       = One(BRESTADM_SESSION)
    image_id  = one.image.allocate(template, 1, False)
    image     = Image(image_id)

    assert image_exist(image_id) == True
    image.delete()



def test_create_datablock_and_check_capacity():
    template = """
        NAME = api_test_image_2
        TYPE = DATABLOCK
        SIZE = 1024000
    """

    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneActionException):
        one.image.allocate(template, 1, True)
    
    

def test_create_datablock_when_datastore_not_exist():
    template = """
        NAME = api_test_image_3
        TYPE = DATABLOCK
        SIZE = 1024000 
    """

    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.allocate(template, 99999)



def test_create_datablock_in_system_datastore():
    template = """
        NAME = api_test_image_4
        TYPE = DATABLOCK
        SIZE = 10 
    """

    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneException):
        one.image.allocate(template, 0)



def test_create_datablock_as_persistent():
    template = """
        NAME = api_test_image_5
        TYPE = DATABLOCK
        SIZE = 100
        PERSISTENT = YES 
    """
    one      = One(BRESTADM_SESSION)
    image_id = one.image.allocate(template, 1)
    image    = Image(image_id)

    assert image.info().PERSISTENT == True
    image.delete()



def test_create_os_image_by_local_path():
    file_path = "/tmp/testfile"
    run_command(COMMAND_EXECUTOR + " " + f"dd if=/dev/urandom of={file_path} bs=1MiB count=10")
    template  = f"""
        NAME = api_test_image_6
        TYPE = OS
        PATH = {file_path}
    """
    one      = One(BRESTADM_SESSION)
    image_id = one.image.allocate(template, 1)
    image    = Image(image_id)

    assert image_exist(image_id) == True
    image.delete()

    run_command(COMMAND_EXECUTOR + " " + f"rm -f {file_path}")
