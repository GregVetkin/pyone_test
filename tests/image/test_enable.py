import pytest

from api                import One
from pyone              import OneServer, OneInternalException, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import create_image_by_tempalte, Image
from one_cli.vm         import create_vm_by_tempalte, VirtualMachine

from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)


IMAGE_STATES = {1: "ГОТОВО",
                2: "ИСПОЛЬЗУЕТСЯ",
                3: "Отключен",} 



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


# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.enable(999999)
    with pytest.raises(OneNoExistsException):
        one.image.disable(999999)



def test_enable_and_disable_used_image(prepare_image_used_by_vm):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image_used_by_vm
    assert image.info().STATE == 2

    with pytest.raises(OneInternalException):
        one.image.disable(image._id)
    assert image.info().STATE == 2

    with pytest.raises(OneInternalException):
        one.image.enable(image._id)
    assert image.info().STATE == 2



def test_enable_enabled_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    assert image.info().STATE == 1
    one.image.enable(image._id)
    assert image.info().STATE == 1



def test_enable_disabled_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    image.disable()

    assert image.info().STATE == 3
    one.image.enable(image._id)
    assert image.info().STATE == 1



def test_disable_disabled_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    image.disable()

    assert image.info().STATE == 3
    one.image.disable(image._id)
    assert image.info().STATE == 3



def test_disable_enabled_image(prepare_image):
    one    = One(BRESTADM_SESSION)
    image  = prepare_image

    assert image.info().STATE == 1
    one.image.disable(image._id)
    assert image.info().STATE == 3

