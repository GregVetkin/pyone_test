import pytest

from api                import One
from pyone              import OneAuthorizationException
from utils              import get_user_auth
from one_cli.vm         import VirtualMachine, create_vm
from one_cli.image      import Image, create_image, wait_image_ready, image_exist
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import delete_undeletable__test

BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def image_datastore():
    datastore_template = """
        NAME   = api_test_image_ds
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
    template = """
        NAME = api_test_image_1
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
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, image_template, True)
    image    = Image(image_id)

    vm_tempalte = f"""
        NAME    = apt_test_vm
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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    delete_if_not_exist__test(one.image)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_delete(one: One, image: Image):
    delete__test(one.image, image)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_used_image_delete(one: One, used_image: Image):
    delete_undeletable__test(one.image, used_image)


#@pytest.mark.skip(reason="Нужна консультация по поводу провала при lock-level 4 (All). И уровне 3")
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
def test_delete_locked_image(one: One, image: Image, lock_level: int):
    image.lock(lock_level)
    with pytest.raises(OneAuthorizationException):
        one.image.delete(image._id)
    assert image_exist(image._id)

