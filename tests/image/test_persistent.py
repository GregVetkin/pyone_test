import pytest

from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils              import get_unic_name
from one_cli.image      import Image, create_image, wait_image_ready
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from one_cli.datastore  import Datastore, create_datastore
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
    wait_image_ready(image_id)
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


@pytest.fixture
def image_with_snapshot(image_datastore: Datastore, system_datastore: Datastore):
    image_template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, image_template, True)
    image    = Image(image_id)
    image.persistent()
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
    vm.create_disk_snapshot(0, get_unic_name())
    wait_vm_offline(vm_id)
    vm.terminate()
    wait_image_ready(image_id)
    yield image
    wait_image_ready(image_id)
    image.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image._persistent(999999)
    with pytest.raises(OneNoExistsException):
        one.image._nonpersistent(999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_used_image_persistencte(one: One, used_image: Image):
    image_info = used_image.info()
    assert image_info.STATE == 2
    start_image_persistence = image_info.PERSISTENT
    
    with pytest.raises(OneInternalException):
        one.image._persistent(used_image._id)
    assert used_image.info().PERSISTENT == start_image_persistence

    with pytest.raises(OneInternalException):
        one.image._nonpersistent(used_image._id)
    assert used_image.info().PERSISTENT == start_image_persistence



@pytest.mark.parametrize("start_persistent", [True, False])
@pytest.mark.parametrize("target_persistence", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_persistent_image(one: One, image: Image, start_persistent: bool, target_persistence: bool):
    if start_persistent:
        image.persistent()
    else:
        image.nonpersistent()
    assert image.info().PERSISTENT == start_persistent

    if target_persistence:
        one.image._persistent(image._id)
    else:
        one.image._nonpersistent(image._id)
    assert image.info().PERSISTENT == target_persistence



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_make_nonpers_image_with_snapshots(one: One, image_with_snapshot: Image):
    assert image_with_snapshot.info().SNAPSHOTS
    with pytest.raises(OneInternalException):
        one.image._nonpersistent(image_with_snapshot._id)
    assert image_with_snapshot.info().PERSISTENT
