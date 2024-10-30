import pytest

from api                import One
from pyone              import OneServer, OneInternalException, OneNoExistsException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, make_image_persistent, wait_image_rdy, get_image_persistence_status
from commands.vm        import create_vm_by_tempalte, delete_vm


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)


ERROR_GETTING_IMAGE                 = "Error getting image"
ERROR_COULD_NOT_MAKE_IMAGE_PERS     = "Could not make image persistent"
ERROR_COULD_NOT_MAKE_IMAGE_NONPERS  = "Could not make image non-persistent"



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






def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException, match=ERROR_GETTING_IMAGE):
        one.image.make_persistent(999999)
        one.image.make_nonpersistent(999999)


def test_make_pers_and_nonpers_used_image(prepare_image_and_vm):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image_and_vm

    with pytest.raises(OneInternalException, match=ERROR_COULD_NOT_MAKE_IMAGE_PERS):
        one.image.make_persistent(image_id)

    with pytest.raises(OneInternalException, match=ERROR_COULD_NOT_MAKE_IMAGE_NONPERS):
        one.image.make_nonpersistent(image_id)



def test_make_pers_pers_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    make_image_persistent(image_id)
    assert get_image_persistence_status(image_id) == "Yes"
    one.image.make_persistent(image_id)
    assert get_image_persistence_status(image_id) == "Yes"


def test_make_pers_nonpers_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_persistence_status(image_id) == "No"
    one.image.make_persistent(image_id)
    assert get_image_persistence_status(image_id) == "Yes"


def test_make_nonpers_nonpers_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_persistence_status(image_id) == "No"
    one.image.make_nonpersistent(image_id)
    assert get_image_persistence_status(image_id) == "No"


def test_make_nonpers_pers_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    make_image_persistent(image_id)
    assert get_image_persistence_status(image_id) == "Yes"
    one.image.make_nonpersistent(image_id)
    assert get_image_persistence_status(image_id) == "No"




