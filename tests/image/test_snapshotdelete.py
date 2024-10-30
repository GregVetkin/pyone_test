import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, wait_image_rdy, make_image_persistent, get_snapshot_id, is_snapshot_exist
from commands.vm        import create_vm_by_tempalte, delete_vm, wait_vm_offline
from utils              import run_command

URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = f"""
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    yield image_id
    delete_image(image_id)


@pytest.fixture
def prepare_image_with_snapshot():
    image_name     = "api_test_image"
    image_template = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id    = create_image_by_tempalte(1, image_template, True)
    make_image_persistent(image_id)
    vm_tempalte = f"""
        NAME    = apt_test_vm
        CPU     = 1
        MEMORY  = 32
        DISK    = [
            IMAGE_ID = {image_id}
        ]
    """
    vm_id       = create_vm_by_tempalte(vm_tempalte, await_vm_offline=True)
    snap_name   = "api_test_disk_snap"
    run_command(f"sudo onevm disk-snapshot-create {vm_id} 0 {snap_name}")
    wait_vm_offline(vm_id)
    delete_vm(vm_id)
    wait_image_rdy(image_id)
    snap_id = get_snapshot_id(image_id, snap_name)

    yield (image_id, image_name), (snap_id, snap_name)

    wait_image_rdy(image_id)
    delete_image(image_id)






def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.snapshotdelete(99999, 0)


def test_image_snapshot_not_exist(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    with pytest.raises(OneActionException):
        one.image.snapshotdelete(image_id, 99999)


def test_delete_image_snapshot(prepare_image_with_snapshot):
    one = One(BRESTADM_SESSION)
    (image_id, _), (snap_id, snap_name) = prepare_image_with_snapshot
    assert is_snapshot_exist(image_id, snap_name) == True
    one.image.snapshotdelete(image_id, snap_id)
    assert is_snapshot_exist(image_id, snap_name) == False
