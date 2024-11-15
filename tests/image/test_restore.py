import pytest
import time
from api                import One
from pyone              import OneNoExistsException, OneException
from utils              import get_unic_name
from one_cli.image      import Image, create_image, image_exist, wait_image_ready
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vm         import VirtualMachine, create_vm, vm_exist
from config             import ADMIN_NAME



@pytest.fixture(scope="module")
def image_datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture(scope="module")
def file_datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture(scope="module")
def system_datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(template)
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
    image.delete()


@pytest.fixture
def backup_image(image_datastore: Datastore, system_datastore: Datastore, file_datastore: Datastore):
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
    vm_id = create_vm(vm_tempalte, await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    vm.backup()
    backup_id = image_id + 2 # +2 Потому что, видимо, сначала делается клон образа, а потом бекап из клона. Клон удаляется

    while not image_exist(backup_id):
        time.sleep(5)

    vm.terminate()
    wait_image_ready(image_id)
    image.delete()
    backup = Image(backup_id)

    yield backup

    backup.delete()
    try:
        vm  = VirtualMachine(vm_id+1)
        img = Image(backup_id+1)
        vm.terminate()
        wait_image_ready(backup_id+1)
        img.delete()
    except Exception as _:
        pass



# =================================================================================================
# TESTS
# =================================================================================================


    
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_backup_image_not_exist(one: One, image_datastore: Datastore):
    with pytest.raises(OneNoExistsException):
        one.image.restore(999999, image_datastore._id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_not_backup_image_type(one: One, image: Image, image_datastore: Datastore):
    assert image.info().TYPE != 6
    with pytest.raises(OneException):
        one.image.restore(image._id, image_datastore._id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One, backup_image: Image):
    assert backup_image.info().TYPE == 6
    with pytest.raises(OneNoExistsException):
        one.image.restore(backup_image._id, 999999)
    time.sleep(10)
    assert not image_exist(backup_image._id + 1)
    assert not vm_exist(int(backup_image.info().TEMPLATE["ONEVMID"]))



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_restore_backup_image_into(one: One, backup_image: Image, image_datastore: Datastore):
    backup_info = backup_image.info()
    assert backup_info.TYPE == 6

    backuped_vm_id      = int(backup_info.TEMPLATE["ONEVMID"])
    restored_vm_id      = backuped_vm_id + 1
    restored_image_id   = backup_image._id + 1

    one.image.restore(backup_image._id, image_datastore._id)
    time.sleep(30)

    assert image_datastore._id == Image(restored_image_id).info().DATASTORE_ID
    assert image_exist(restored_image_id)
    assert vm_exist(restored_vm_id)
