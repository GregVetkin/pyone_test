import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException
from utils              import get_brestadm_auth
from commands.image     import is_image_exist, delete_image, create_image_by_tempalte, wait_image_rdy
from commands.vm        import create_vm_by_tempalte, delete_vm

from config             import API_URI


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield image_id

    try:
        delete_image(image_id)
    except Exception as _:
        pass


@pytest.fixture
def prepare_image_and_vm():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id    = create_image_by_tempalte(1, image_template, True)
    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)

    yield image_id

    delete_vm(vm_id)
    wait_image_rdy(image_id)
    delete_image(image_id)


# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.delete(999999)
    

def test_unused_image_deleted(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    one.image.delete(image_id)
    assert is_image_exist(image_id) == False


def test_used_image_delete(prepare_image_and_vm):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image_and_vm

    with pytest.raises(OneActionException):
        one.image.delete(image_id)

    assert is_image_exist(image_id) == True

