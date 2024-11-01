import pytest

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
def prepare_image_with_snapshot():
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
    vm.create_disk_snapshot(0, "api_test_disk_snap")
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
        one.image.snapshotdelete(99999, 0)


def test_image_snapshot_not_exist(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image
    
    with pytest.raises(OneActionException):
        one.image.snapshotdelete(image._id, 99999)


def test_delete_image_snapshot(prepare_image_with_snapshot):
    one     = One(BRESTADM_SESSION)
    image   = prepare_image_with_snapshot
    snap_id = image.info().SNAPSHOTS[0].ID

    one.image.snapshotdelete(image._id, snap_id)

    for spanshot in image.info().SNAPSHOTS:
        assert spanshot.ID != snap_id

