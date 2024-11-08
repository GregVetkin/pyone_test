import pytest

from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.vm         import VirtualMachine, create_vm_by_tempalte, wait_vm_offline
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
def image_datastore():
    template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def system_datastore():
    template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_ds_by_tempalte(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(image_datastore: Datastore):
    template = """
        NAME = api_test_datablock
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(image_datastore._id, template)
    image    = Image(image_id)
    yield image
    image.wait_ready_status()
    image.delete()
    

@pytest.fixture
def used_image(image_datastore: Datastore):
    image_template = """
        NAME = api_test_used_datablock
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
def image_with_snapshot(image_datastore: Datastore, system_datastore: Datastore):
    image_template = """
        NAME = api_test_datablock_with_snap
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(image_datastore._id, image_template, True)
    image    = Image(image_id)
    image.make_persistent()
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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.make_persistent(999999)
    with pytest.raises(OneNoExistsException):
        one.image.make_nonpersistent(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_used_image_persistencte(one: One, used_image: Image):
    image_info = used_image.info()
    assert image_info.STATE == 2
    start_image_persistence = image_info.PERSISTENT
    
    with pytest.raises(OneInternalException):
        one.image.make_persistent(used_image._id)
    assert used_image.info().PERSISTENT == start_image_persistence

    with pytest.raises(OneInternalException):
        one.image.make_nonpersistent(used_image._id)
    assert used_image.info().PERSISTENT == start_image_persistence



@pytest.mark.parametrize("start_persistent", [True, False])
@pytest.mark.parametrize("target_persistence", [True, False])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_persistent_image(one: One, image: Image, start_persistent: bool, target_persistence: bool):
    if start_persistent:
        image.make_persistent()
    else:
        image.make_nonpersistent()
    assert image.info().PERSISTENT == start_persistent

    if target_persistence:
        one.image.make_persistent(image._id)
    else:
        one.image.make_nonpersistent(image._id)
    assert image.info().PERSISTENT == target_persistence



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_make_nonpers_image_with_snapshots(one: One, image_with_snapshot: Image):
    assert image_with_snapshot.info().SNAPSHOTS
    with pytest.raises(OneInternalException):
        one.image.make_nonpersistent(image_with_snapshot._id)
    assert image_with_snapshot.info().PERSISTENT
