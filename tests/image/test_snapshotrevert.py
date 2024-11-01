import pytest
import random

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.vm         import VirtualMachine, create_vm_by_tempalte, wait_vm_offline
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)




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
def prepare_image_with_5_snapshots():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
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

    for _ in range(5):
        vm.create_disk_snapshot(0, f"api_test_disk_snap_{_}")
        wait_vm_offline(vm_id)

    vm.terminate()
    image.wait_ready_status()

    yield image

    image.wait_ready_status()
    image.delete()




# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.snapshotrevert(99999, 0)



def test_image_snapshot_not_exist(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image
    
    with pytest.raises(OneActionException):
        one.image.snapshotrevert(image._id, 99999)



def test_revert_image_snapshot(prepare_image_with_5_snapshots):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_5_snapshots

    not_active_snap_ids = [snapshot.ID for snapshot in image.info().SNAPSHOTS if not snapshot.ACTIVE]
    snap_id             = random.choice(not_active_snap_ids)

    one.image.snapshotrevert(image._id, snap_id)
    active_snap_id = next(snapshot.ID for snapshot in image.info().SNAPSHOTS if snapshot.ACTIVE)
    assert active_snap_id == snap_id



def test_image_snapshtod_already_active(prepare_image_with_5_snapshots):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_5_snapshots

    active_snap_id = next(snapshot.ID for snapshot in image.info().SNAPSHOTS if snapshot.ACTIVE)
    with pytest.raises(OneActionException):
        one.image.snapshotrevert(image._id, active_snap_id)