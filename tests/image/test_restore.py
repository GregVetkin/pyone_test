import pytest
import time

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException, OneException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte, image_exist
from one_cli.vm         import VirtualMachine, create_vm_by_tempalte, vm_exist

from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)


@pytest.fixture
def prepare_image():
    image_template = """
        NAME = api_test_datablock
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)
    
    yield image

    image.delete()



@pytest.fixture
def prepare_backup_image():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id    = create_image_by_tempalte(1, image_template, True)
    image       = Image(image_id)
    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)
    vm    = VirtualMachine(vm_id)

    vm.backup()
    backup_id = image_id + 2

    while not image_exist(backup_id):
        time.sleep(5)

    vm.terminate()
    image.wait_ready_status()
    image.delete()

    backup = Image(backup_id)
    
    yield backup

    backup.delete()

    try:
        vm  = VirtualMachine(vm_id+1)
        img = Image(backup_id+1)
        vm.terminate()
        img.wait_ready_status()
        img.delete()

    except Exception as _:
        pass




# =================================================================================================
# TESTS
# =================================================================================================


    

def test_backup_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.restore(999999, 1)



def test_datastore_not_exist(prepare_backup_image):
    one    = One(BRESTADM_SESSION)
    backup = prepare_backup_image
    with pytest.raises(OneNoExistsException):
        one.image.restore(backup._id, 999999)



def test_not_backup_image_type(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image
    with pytest.raises(OneException):
        one.image.restore(image._id, 1)
    


def test_restore_backup_image(prepare_backup_image):
    one = One(BRESTADM_SESSION)
    backup = prepare_backup_image
    backup_info = backup.info()
    backuped_vm_id = int(backup_info.TEMPLATE["ONEVMID"])
    restored_vm_id = backuped_vm_id + 1
    restored_image_id = backup._id + 1

    one.image.restore(backup._id, 1)

    while not vm_exist(restored_vm_id):
        time.sleep(5)
    
    assert image_exist(restored_image_id)
    assert vm_exist(restored_vm_id)
