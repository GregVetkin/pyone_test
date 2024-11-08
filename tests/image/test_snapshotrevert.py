import pytest
import random

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from one_cli.image      import Image, create_image, wait_image_ready
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM



BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def image_datastore():
    template = """
        NAME   = api_test_image_ds
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
    template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(template)
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
    image_id = create_image(image_datastore._id, template)
    image    = Image(image_id)
    yield image
    wait_image_ready(image_id)
    image.delete()
    

@pytest.fixture
def image_with_snapshots(image_datastore: Datastore, system_datastore: Datastore):
    image_template = """
        NAME = api_test_datablock_with_snaps
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(image_datastore._id, image_template, True)
    image    = Image(image_id)
    image.persistent()
    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id = create_vm(vm_tempalte, await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    for _ in range(5):
        vm.create_disk_snapshot(0, f"api_test_disk_snap_{_}")
        wait_vm_offline(vm_id)
    vm.terminate()
    wait_image_ready(image_id)
    yield image
    wait_image_ready(image_id)
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.snapshotrevert(99999, 0)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_snapshot_not_exist(one: One, image: Image):
    with pytest.raises(OneActionException):
        one.image.snapshotrevert(image._id, 99999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_revert_image_snapshot(one: One, image_with_snapshots: Image):
    image_snapshots = image_with_snapshots.info().SNAPSHOTS
    assert len(image_snapshots) > 1
    not_active_snap_ids = [snapshot.ID for snapshot in image_snapshots if not snapshot.ACTIVE]
    target_snap_id = random.choice(not_active_snap_ids)
    one.image.snapshotrevert(image_with_snapshots._id, target_snap_id)
    new_active_snap_id = next(snapshot.ID for snapshot in image_with_snapshots.info().SNAPSHOTS if snapshot.ACTIVE)
    assert new_active_snap_id == target_snap_id



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_snapshtod_already_active(one: One, image_with_snapshots: Image):
    image_snapshots = image_with_snapshots.info().SNAPSHOTS
    assert len(image_snapshots) > 1
    active_snap_id = next(snapshot.ID for snapshot in image_snapshots if snapshot.ACTIVE)
    with pytest.raises(OneActionException):
        one.image.snapshotrevert(image_with_snapshots._id, active_snap_id)
    new_active_snap_id = next(snapshot.ID for snapshot in image_with_snapshots.info().SNAPSHOTS if snapshot.ACTIVE)
    assert active_snap_id == new_active_snap_id
