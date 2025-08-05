import pytest
import time
import pyone
import random

from utils.version      import Version
from api                import One
from config.opennebula  import ImageStates, VmStates, VmRecoverOperations, ImageTypes
from config.base        import BREST_VERSION
from utils.other        import wait_until, get_unic_name
from utils.connection   import brest_admin_ssh_conn
from utils.commands     import run_command_via_ssh



@pytest.fixture
def file_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template, -1)
    time.sleep(3)

    yield datastore_id

    one.datastore.delete(datastore_id)
    time.sleep(3)


@pytest.fixture
def backup_datastore(one: One):
    template = f"""
        NAME={get_unic_name()}
        DS_MAD=rsync
        RSYNC_HOST=10.0.70.21
        RSYNC_USER=oneadmin
        TYPE=BACKUP_DS
    """
    datastore_id = one.datastore.allocate(template, -1)
    time.sleep(3)

    yield datastore_id

    one.datastore.delete(datastore_id)
    time.sleep(3)



@pytest.fixture(params=[
    pytest.param("backup_datastore", marks=pytest.mark.skipif( Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")),
    pytest.param("file_datastore",   marks=pytest.mark.skipif( Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only"))
])
def backup_image(one: One, poweroff_vm_mini: int, request):
    vm_id = poweroff_vm_mini
    backup_ds_id = request.getfixturevalue(request.param)

    run_command_via_ssh(brest_admin_ssh_conn, f"onevm backup {vm_id} -d {backup_ds_id}")

    if Version(BREST_VERSION) < Version("4"):
        time.sleep(120)
    else:
        time.sleep(20)

    backups = [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE if image.TYPE == ImageTypes.BACKUP]
    backup_id = max(backups)

    yield backup_id

    one.image.delete(backup_id, True)
    wait_until(lambda: backup_id not in [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE])



# =================================================================================================
# TESTS
# =================================================================================================




def test_backup_image_not_exist(one: One, dummy_datastore: int):
    image_id = random.randint(9999, 999999)
    datastore_id = dummy_datastore
    vm_name = get_unic_name()

    with pytest.raises(pyone.OneNoExistsException):
        one.image.restore(image_id, datastore_id, vm_name)


def test_wrong_image_type(one: One, dummy_image: int, dummy_datastore: int):
    image_id = dummy_image
    datastore_id = dummy_datastore
    vm_name = get_unic_name()

    assert one.image.info(image_id, False).TYPE != ImageTypes.BACKUP

    with pytest.raises(pyone.OneActionException):
        one.image.restore(image_id, datastore_id, vm_name)



def test_backup_datastore_not_exist(one: One, backup_image: int):
    image_id = backup_image
    datastore_id = random.randint(9999, 999999)
    vm_name = get_unic_name()

    assert one.image.info(image_id).TYPE == ImageTypes.BACKUP

    with pytest.raises(pyone.OneNoExistsException):
        one.image.restore(image_id, datastore_id, vm_name)




@pytest.mark.skipif(Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only")
def test_restore_into_certain_storage_v3(one: One, backup_image: int, dummy_datastore: int):
    image_id     = backup_image
    datastore_id = dummy_datastore
    vm_name      = get_unic_name()

    backup_info = one.image.info(image_id, False)

    backuped_vm_id      = int(backup_info.TEMPLATE["ONEVMID"])
    restored_vm_id      = backuped_vm_id + 1
    restored_image_id   = backup_image + 1

    one.image.restore(backup_image, datastore_id, vm_name)
    wait_until(
        lambda: restored_vm_id in [vm.ID for vm in one.vmpool.info(-2, -1, -1, -2, "").VM],
        timeout=120,
        timeout_message=f"Превышено время ожидания появления восстановленной ВМ {restored_vm_id}"
        )

    assert one.vm.info(restored_vm_id, False).NAME == vm_name

    one.vm.recover(restored_vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(restored_vm_id, False).STATE == VmStates.DONE)
    
    assert one.image.info(restored_image_id, False).DATASTORE_ID == datastore_id

    one.image.delete(restored_image_id, True)
    wait_until(lambda: restored_image_id not in [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE])




# @pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
# def test_restore_without_template(one: One, backup_image: int, dummy_datastore: int):
#     image_id             = backup_image
#     datastore_id         = dummy_datastore
#     backup_info          = one.image.info(image_id)
#     vm_id                = backup_info.VMS.ID[-1]
#     api_response         = one.image.restore(backup_image, datastore_id)
#     ids                  = [int(_id) for _id in api_response.split()]
#     restored_template_id = ids[0]
#     restored_image_ids   = ids[1:]

#     time.sleep(30)

#     assert one.template.info(restored_template_id).NAME.startswith(str(vm_id))

#     for restored_image_id in restored_image_ids:
#         assert one.image.info(restored_image_id).NAME.startswith(str(vm_id))

#     one.template.delete(restored_template_id, delete_images=True)

#     time.sleep(10)



# @pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
# def test_restore_with_template(one: One, backup_image: int, dummy_datastore: int):
#     image_id             = backup_image
#     datastore_id         = dummy_datastore
#     name                 = get_unic_name()
#     template             = f"NAME={name}"
#     backup_info          = one.image.info(backup_image)
#     vm_id                = backup_info.VMS.ID[-1]
#     api_response         = one.image.restore(image_id, datastore_id, template)
#     ids                  = [int(_id) for _id in api_response.split()]
#     restored_template_id = ids[0]
#     restored_image_ids   = ids[1:]

#     time.sleep(30)

#     assert one.template.info(restored_template_id).NAME == name

#     for restored_image_id in restored_image_ids:
#         assert one.image.info(restored_image_id).NAME.startswith(f"{name}-disk-")

#     one.template.delete(restored_template_id, delete_images=True)

#     time.sleep(10)