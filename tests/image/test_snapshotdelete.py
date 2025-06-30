import pytest
import time
from api                import One
from pyone              import OneNoExistsException, OneActionException, OneException
from utils              import get_unic_name
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline
from one_cli.image      import Image, create_image, wait_image_ready
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
def image_with_snapshots(image_datastore: Datastore, system_datastore: Datastore):
    image_template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
        PERSISTENT = YES
    """
    image_id = create_image(image_datastore._id, image_template, True)
    image    = Image(image_id)
    # image.persistent()
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

    for _ in range(3):
        vm.create_disk_snapshot(0, get_unic_name())
        time.sleep(10)


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
        one.image.snapshotdelete(99999, 0)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_snapshot_not_exist(one: One, image: Image):
    with pytest.raises(OneActionException):
        one.image.snapshotdelete(image._id, 99999)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unactive_snapshot(one: One, image_with_snapshots: Image):
    image_id    = image_with_snapshots._id
    snapshots   = one.image.info(image_id).SNAPSHOTS.SNAPSHOT

    no_parent_snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.PARENT == -1))
    one.image.snapshotrevert(image_id, no_parent_snapshot_id)
    time.sleep(5)

    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (not snapshot.CHILDREN)))

    _id = one.image.snapshotdelete(image_id, snapshot_id)
    assert _id == snapshot_id
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id not in snapshots_ids




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_active_snapshot(one: One, image_with_snapshots: Image):
    image_id    = image_with_snapshots._id
    snapshots   = one.image.info(image_id).SNAPSHOTS.SNAPSHOT

    snapshot_id = next((snapshot.ID for snapshot in snapshots if snapshot.ACTIVE))

    with pytest.raises(OneException):
        one.image.snapshotdelete(image_id, snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id in snapshots_ids




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_snapshot_with_children(one: One, image_with_snapshots: Image):
    image_id    = image_with_snapshots._id
    snapshots   = one.image.info(image_id).SNAPSHOTS.SNAPSHOT

    snapshot_id = next((snapshot.ID for snapshot in snapshots if (not snapshot.ACTIVE) and (snapshot.CHILDREN)))

    with pytest.raises(OneException):
        one.image.snapshotdelete(image_id, snapshot_id)
    
    time.sleep(5)
    
    snapshots_ids = [snapshot.ID for snapshot in one.image.info(image_id).SNAPSHOTS.SNAPSHOT]
    assert snapshot_id in snapshots_ids
    


