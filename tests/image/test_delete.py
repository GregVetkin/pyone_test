import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException
from utils              import get_user_auth
from one_cli.vm         import create_vm_by_tempalte, VirtualMachine
from one_cli.image      import create_image_by_tempalte, Image, image_exist
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)

    yield image

    try:
        image.delete()
    except Exception as _:
        pass



@pytest.fixture
def prepare_image_used_by_vm():
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
    vm_id   = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)
    vm      = VirtualMachine(vm_id)

    yield image

    vm.terminate()
    image.wait_ready_status()
    image.delete()


# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one  = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.delete(999999)
    

def test_unused_image_deleted(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    one.image.delete(image._id)
    assert image_exist(image._id) == False


def test_used_image_delete(prepare_image_used_by_vm):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_used_by_vm

    with pytest.raises(OneActionException):
        one.image.delete(image._id)
    assert image_exist(image._id) == True

