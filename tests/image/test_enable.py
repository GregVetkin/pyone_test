import pytest

from api                import One
from pyone              import OneServer, OneInternalException, OneNoExistsException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, get_image_state, disable_image, wait_image_rdy
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

    delete_image(image_id)
    

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
        one.image.enable(999999)
        one.image.disable(999999)


def test_enable_and_disable_used_image(prepare_image_and_vm):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image_and_vm
    assert get_image_state(image_id) == "used"
    with pytest.raises(OneInternalException):
        one.image.disable(image_id)
        one.image.enable(image_id)


def test_enable_enabled_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    one.image.enable(image_id)
    assert get_image_state(image_id) == "rdy"


def test_enable_disabled_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    disable_image(image_id)
    assert get_image_state(image_id) == "disa"
    one.image.enable(image_id)
    assert get_image_state(image_id) == "rdy"


def test_disable_disabled_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    disable_image(image_id)
    assert get_image_state(image_id) == "disa"
    one.image.disable(image_id)
    assert get_image_state(image_id) == "disa"


def test_disable_enabled_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_state(image_id) == "rdy"
    one.image.disable(image_id)
    assert get_image_state(image_id) == "disa"

