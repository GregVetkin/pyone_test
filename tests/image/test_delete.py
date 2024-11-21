import pytest

from api                import One
from utils              import get_unic_name
from one_cli.vm         import VirtualMachine, create_vm
from one_cli.image      import Image, create_image, wait_image_ready, image_exist
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test



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

    if not image_exist(image_id):
        return
    
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
    delete_if_not_exist__test(one.image)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_delete(one: One, image: Image):
    delete__test(one.image, image)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_used_image_delete(one: One, used_image: Image):
    cant_be_deleted__test(one.image, used_image)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_delete_locked_image(one: One, image: Image, lock_level: int):
    image.lock(lock_level)
    if lock_level == 3:
        delete__test(one.image, image)
    else:
        cant_be_deleted__test(one.image, image)

