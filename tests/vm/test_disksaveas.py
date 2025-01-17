import pytest

from time               import sleep
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image, image_exist
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vm         import VirtualMachine, create_vm, wait_vm_offline, vm_exist
from config             import ADMIN_NAME




# @pytest.fixture(scope="module")
# def image_datastore():
#     datastore_template = f"""
#         NAME   = {get_unic_name()}
#         TYPE   = IMAGE_DS
#         TM_MAD = ssh
#         DS_MAD = fs
#     """
#     datastore_id = create_datastore(datastore_template)
#     datastore    = Datastore(datastore_id)
#     yield datastore
#     datastore.delete()


# @pytest.fixture(scope="module")
# def system_datastore():
#     datastore_template = f"""
#         NAME   = {get_unic_name()}
#         TYPE   = SYSTEM_DS
#         TM_MAD = ssh
#     """
#     datastore_id = create_datastore(datastore_template)
#     datastore    = Datastore(datastore_id)
#     yield datastore
#     datastore.delete()


# @pytest.fixture(scope="module")
# def image(image_datastore: Datastore):
#     template = f"""
#         NAME = {get_unic_name()}
#         TYPE = DATABLOCK
#         SIZE = 10
#     """
#     image_id = create_image(image_datastore._id, template)
#     image    = Image(image_id)
#     yield image
#     image.delete()


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 10
    """
    ds_id = 1
    for ds in one.datastorepool.info().DATASTORE:
        if ds.NAME.startswith("image_"):
            ds_id = ds.ID
            break

    image_id = create_image(ds_id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture()
def vm_with_disk(image: Image):
    vm_id = create_vm(f"CPU=1\nMEMORY=1\nDISK=[IMAGE_ID={image._id}]", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.disk_detach(0)
    wait_vm_offline(vm_id)
    vm.terminate()
    while vm_exist(vm_id):
        sleep(2)
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    saved_disk_name = get_unic_name()
    with pytest.raises(OneException):
        one.vm.disksaveas(9999999, 0, saved_disk_name, "", -1)



# @pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
# def test_disk_not_exist(one: One, vm_with_disk: VirtualMachine):
#     saved_disk_name = get_unic_name()
#     with pytest.raises(OneException):
#         one.vm.disksaveas(vm_with_disk._id, 999999, saved_disk_name, "", -1)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disk_name_is_already_taken(one: One, vm_with_disk: VirtualMachine):
    image_id = int(one.vm.info(vm_with_disk._id).TEMPLATE["DISK"]["IMAGE_ID"])
    saved_disk_name = one.image.info(image_id).NAME
    one.image.chown(image_id, 2, -1)

    with pytest.raises(OneException):
        one.vm.disksaveas(vm_with_disk._id, 0, saved_disk_name, "", -1)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disksaveas__cold(one: One, vm_with_disk: VirtualMachine):
    assert one.vm.info(vm_with_disk._id).STATE == 8

    saved_disk_name = get_unic_name()
    _id = one.vm.disksaveas(vm_with_disk._id, 0, saved_disk_name, "", -1)

    assert one.image.info(_id).NAME == saved_disk_name
    one.image.delete(_id)
