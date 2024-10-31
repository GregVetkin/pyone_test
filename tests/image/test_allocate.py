import pytest

from api    import One
from pyone  import OneServer, OneActionException, OneNoExistsException, OneException
from utils  import get_brestadm_auth, run_command

from config import API_URI



BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)




# =================================================================================================
# TESTS
# =================================================================================================


def test_create_datablock_and_dont_check_capacity():
    disk_name   = "test_create_datablock_and_dont_check_capacity"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "DATABLOCK"
        SIZE = "1024000"  
    """

    one = One(BRESTADM_SESSION)
    one.image.allocate(template, 1, False)
    run_command(f"sudo oneimage delete {disk_name}")


def test_create_datablock_and_check_capacity():
    disk_name   = "test_create_datablock_and_check_capacity"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "DATABLOCK"
        SIZE = "1024000"  
    """
    one = One(BRESTADM_SESSION)

    with pytest.raises(OneActionException, match="Not enough space in datastore"):
        one.image.allocate(template, 1, True)


def test_create_datablock_when_datastore_not_exist():
    disk_name   = "test_create_datablock_when_datastore_not_exist"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "DATABLOCK"
        SIZE = "1024000"  
    """
    one = One(BRESTADM_SESSION)

    with pytest.raises(OneNoExistsException, match="Error getting datastore"):
        one.image.allocate(template, 99999)


def test_create_datablock_in_system_datastore():
    disk_name   = "test_create_datablock_in_system_datastore"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "DATABLOCK"
        SIZE = "100"  
    """
    one = One(BRESTADM_SESSION)

    with pytest.raises(OneException, match="New images cannot be allocated in a system datastore"):
        one.image.allocate(template, 0)


def test_create_datablock_as_persistent():
    disk_name   = "test_create_datablock_as_persistent"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "DATABLOCK"
        SIZE = "100"
        PERSISTENT = "YES" 
    """
    one = One(BRESTADM_SESSION)
    one.image.allocate(template, 1)

    persistence = run_command(f"sudo oneimage show {disk_name} | grep PERSISTENT " + " | awk '{print $3}'")
    assert persistence == "Yes"
    run_command(f"sudo oneimage delete {disk_name}")


def test_create_os_image_by_local_path():
    disk_name   = "test_create_os_image_by_local_path"
    file_path   = "/tmp/testfile"
    template    = f"""
        NAME = "{disk_name}"
        TYPE = "OS"
        PATH = "{file_path}"
    """
    run_command(f"sudo dd if=/dev/urandom of=/tmp/testfile bs=1MiB count=50")

    one = One(BRESTADM_SESSION)
    one.image.allocate(template, 1)

    run_command(f"sudo oneimage delete {disk_name}")
    run_command(f"sudo rm -f {file_path}")
