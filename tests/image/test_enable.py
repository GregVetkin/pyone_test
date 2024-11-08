import pytest

from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import create_image_by_tempalte, Image
from one_cli.vm         import create_vm_by_tempalte, VirtualMachine
from one_cli.datastore  import create_ds_by_tempalte, Datastore
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)
IMAGE_STATES = {1: "ГОТОВО",
                2: "ИСПОЛЬЗУЕТСЯ",
                3: "Отключен",} 



@pytest.fixture
def image_datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(image_datastore: Datastore):
    template = """
        NAME = api_test_image_1
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(image_datastore._id, template)
    image    = Image(image_id)

    yield image

    if image.info().LOCK is not None:
        image.unlock()

    image.delete()


@pytest.fixture
def used_image(image_datastore: Datastore):
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(image_datastore._id, image_template, True)
    image    = Image(image_id)

    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id = create_vm_by_tempalte(vm_tempalte, await_vm_offline=False)
    vm    = VirtualMachine(vm_id)

    yield image

    vm.terminate()
    image.wait_ready_status()
    image.delete()


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
    



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.enable(999999)
    with pytest.raises(OneNoExistsException):
        one.image.disable(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_and_disable_used_image(one: One, used_image: Image):
    assert used_image.info().STATE == 2

    with pytest.raises(OneInternalException):
        one.image.disable(used_image._id)
    assert used_image.info().STATE == 2
    
    with pytest.raises(OneInternalException):
        one.image.enable(used_image._id)
    assert used_image.info().STATE == 2



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_enabled_image(one: One, image: Image):
    assert image.info().STATE == 1
    one.image.enable(image._id)
    assert image.info().STATE == 1



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_enable_disabled_image(one: One, image: Image):
    image.disable()
    assert image.info().STATE == 3
    one.image.enable(image._id)
    assert image.info().STATE == 1



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_disable_disabled_image(one: One, image: Image):
    image.disable()
    assert image.info().STATE == 3
    one.image.disable(image._id)
    assert image.info().STATE == 3



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_disable_enabled_image(one: One, image: Image):
    assert image.info().STATE == 1
    one.image.disable(image._id)
    assert image.info().STATE == 3
