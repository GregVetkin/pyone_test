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
def file_ds(one: One):
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
def rsync_backup_ds(one: One):
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
    pytest.param("rsync_backup_ds",  marks=pytest.mark.skipif( Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")),
    pytest.param("file_ds",          marks=pytest.mark.skipif( Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only"))
])
def backup_image(one: One, poweroff_vm_mini: int, request):
    vm_id = poweroff_vm_mini
    backup_ds_id = request.getfixturevalue(request.param)

    run_command_via_ssh(brest_admin_ssh_conn, f"onevm backup {vm_id} -d {backup_ds_id}")

    time.sleep(120)

    backups = [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE if image.TYPE == ImageTypes.BACKUP]
    backup_id = max(backups)

    yield backup_id

    one.image.delete(backup_id, True)
    wait_until(lambda: backup_id not in [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE])



# =================================================================================================
# TESTS
# =================================================================================================

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# В Brest 3.x метод one.image.restore принимает аргументы one.image.restore(image_id, datastore_id, vm_name)
# Однако в Brest 4.x метод работает иначе и принимает вместо vm_name - шаблон с параметрами (см. документацию 6.8)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def test_backup_image_not_exist(one: One, dummy_datastore: int):
    image_id = random.randint(9999, 999999)
    datastore_id = dummy_datastore
    template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.image.restore(image_id, datastore_id, template)


def test_wrong_image_type(one: One, dummy_image: int, dummy_datastore: int):
    image_id = dummy_image
    datastore_id = dummy_datastore
    vm_name = ""

    assert one.image.info(image_id, False).TYPE != ImageTypes.BACKUP

    with pytest.raises(pyone.OneActionException):
        one.image.restore(image_id, datastore_id, vm_name)



def test_backup_datastore_not_exist(one: One, backup_image: int):
    image_id = backup_image
    datastore_id = random.randint(9999, 999999)
    template = ""

    assert one.image.info(image_id, False).TYPE == ImageTypes.BACKUP

    with pytest.raises(pyone.OneNoExistsException):
        one.image.restore(image_id, datastore_id, template)




@pytest.mark.skipif(Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only")
def test_restore_Brest_3(one: One, backup_image: int, dummy_datastore: int):
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





@pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
def test_restore_Brest_4(one: One, backup_image: int, dummy_datastore: int):
    image_id     = backup_image
    datastore_id = dummy_datastore

    name = get_unic_name()

    template = f"""
        NAME    = {name}
        NO_IP   = YES
        NO_NIC  = YES
    """

    # RETURNS: Blank separated list of restored objects IDs. The first one is the VM Template ID.
    # Сейчас возвращает первым не id шаблона, а ВМ
    api_response = one.image.restore(image_id, datastore_id, template)

    ids = [int(_id) for _id in api_response.split()]

    restored_vm_id = ids[0]
    restored_image_ids = ids[1:]

    time.sleep(60)

    vm_info = one.vm.info(restored_vm_id, False)
    restored_template_id = int(vm_info.TEMPLATE["TEMPLATE_ID"])
    template_info = one.template.info(restored_template_id, False, False)

    assert template_info.NAME == name
    assert vm_info.NAME == f"{name}-{restored_vm_id}"


    for restored_image_id in restored_image_ids:
        image_info = one.image.info(restored_image_id, False)
        assert image_info.NAME.startswith(f"{name}-disk")
        assert image_info.DATASTORE_ID == datastore_id

    one.vm.recover(restored_vm_id, VmRecoverOperations.DELETE)
    time.sleep(10)
    one.template.delete(restored_template_id, delete_images=True)
    time.sleep(10)





# @pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
# def test_restore_without_template(one: One, backup_image: int, dummy_datastore: int):
#     image_id     = backup_image
#     datastore_id = dummy_datastore
#     template     = ""

#     backup_info = one.image.info(image_id, False)
#     vm_id = backup_info.VMS.ID[-1]

#     api_response = one.image.restore(backup_image, datastore_id, template)

#     ids = [int(_id) for _id in api_response.split()]

#     restored_template_id = ids[0]
#     restored_image_ids   = ids[1:]

#     time.sleep(60)

#     assert one.template.info(restored_template_id, False, False).NAME.startswith(str(vm_id))

#     for restored_image_id in restored_image_ids:
#         assert one.image.info(restored_image_id, False).NAME.startswith(str(vm_id))

#     one.template.delete(restored_template_id, delete_images=True)

#     time.sleep(10)

