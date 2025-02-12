import pytest

from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils              import get_unic_name
from one_cli.image      import Image, create_image, wait_image_ready
from one_cli.vm         import VirtualMachine, create_vm
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME


IMAGE_STATES = {1: "ГОТОВО",
                2: "ИСПОЛЬЗУЕТСЯ",
                3: "Отключен",} 


@pytest.fixture(scope="module")
def image_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(image_datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, template)
    image    = Image(image_id)

    yield image

    if image.info().LOCK is not None:
        image.unlock()

    image.delete()


@pytest.fixture
def used_image(image_datastore: Datastore):
    image_template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, image_template, True)
    image    = Image(image_id)

    vm_tempalte = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id = create_vm(vm_tempalte, await_vm_offline=False)
    vm    = VirtualMachine(vm_id)

    yield image

    vm.terminate()
    wait_image_ready(image_id)
    image.delete()





# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image._enable(999999)
    with pytest.raises(OneNoExistsException):
        one.image._disable(999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_and_disable_used_image(one: One, used_image: Image):
    assert used_image.info().STATE == 2

    with pytest.raises(OneInternalException):
        one.image._disable(used_image._id)
    assert used_image.info().STATE == 2
    
    with pytest.raises(OneInternalException):
        one.image._enable(used_image._id)
    assert used_image.info().STATE == 2



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_enabled_image(one: One, image: Image):
    assert image.info().STATE == 1
    one.image._enable(image._id)
    assert image.info().STATE == 1



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_enable_disabled_image(one: One, image: Image):
    image.disable()
    assert image.info().STATE == 3
    one.image._enable(image._id)
    assert image.info().STATE == 1



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disable_disabled_image(one: One, image: Image):
    image.disable()
    assert image.info().STATE == 3
    one.image._disable(image._id)
    assert image.info().STATE == 3



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disable_enabled_image(one: One, image: Image):
    assert image.info().STATE == 1
    one.image._disable(image._id)
    assert image.info().STATE == 3
