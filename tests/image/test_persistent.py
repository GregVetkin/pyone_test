import pytest

from api                import One
from pyone              import OneServer, OneInternalException, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.vm         import VirtualMachine, create_vm_by_tempalte, wait_vm_offline
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

    image.delete()
    

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
    vm_id = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    
    yield image

    vm.terminate()
    image.wait_ready_status()
    image.delete()


@pytest.fixture
def prepare_image_with_snapshot():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id    = create_image_by_tempalte(1, image_template, True)
    image       = Image(image_id)
    image.make_persistent()

    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id  = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)
    vm     = VirtualMachine(vm_id)
    vm.create_disk_snapshot(0, "api_test_snapshot")

    wait_vm_offline(vm_id)
    vm.terminate()
    image.wait_ready_status()

    yield image

    image.wait_ready_status()
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.make_persistent(999999)
        one.image.make_nonpersistent(999999)



def test_make_pers_and_nonpers_used_image(prepare_image_used_by_vm):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_used_by_vm

    with pytest.raises(OneInternalException):
        one.image.make_persistent(image._id)

    with pytest.raises(OneInternalException):
        one.image.make_nonpersistent(image._id)



def test_make_pers_pers_image(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    if not image.info().PERSISTENT:
        image.make_persistent()  

    assert image.info().PERSISTENT == True
    one.image.make_persistent(image._id)
    assert image.info().PERSISTENT == True



def test_make_pers_nonpers_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    assert image.info().PERSISTENT == False
    one.image.make_persistent(image._id)
    assert image.info().PERSISTENT == True



def test_make_nonpers_nonpers_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    assert image.info().PERSISTENT == False
    one.image.make_nonpersistent(image._id)
    assert image.info().PERSISTENT == False



def test_make_nonpers_pers_image(prepare_image):
    one     = One(BRESTADM_SESSION)
    image   = prepare_image

    if not image.info().PERSISTENT:
        image.make_persistent()

    assert image.info().PERSISTENT == True
    one.image.make_nonpersistent(image._id)
    assert image.info().PERSISTENT == False



def test_make_nonpers_image_with_snapshots(prepare_image_with_snapshot):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image_with_snapshot

    assert image.info().PERSISTENT == True
    with pytest.raises(OneInternalException):
        one.image.make_nonpersistent(image._id)
    assert image.info().PERSISTENT == True

