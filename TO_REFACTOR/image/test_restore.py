import pytest
import time

from utils.version      import Version
from api                import One
from pyone              import OneNoExistsException, OneException
from config.opennebula  import ImageStates, VmStates
from config.base        import BREST_VERSION
from utils.other        import wait_until, get_unic_name
from utils.connection   import brest_admin_ssh_conn
from utils.commands     import run_command_via_ssh


@pytest.fixture
def image_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template)
    time.sleep(3)

    yield datastore_id

    one.datastore.delete(datastore_id)
    time.sleep(3)


@pytest.fixture
def file_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template)
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
    datastore_id = one.datastore.allocate(template)
    time.sleep(3)

    yield datastore_id

    one.datastore.delete(datastore_id)
    time.sleep(3)


@pytest.fixture
def system_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = one.datastore.allocate(template)
    time.sleep(3)

    yield datastore_id

    one.datastore.delete(datastore_id)
    time.sleep(3)


@pytest.fixture
def image(one: One, image_datastore: int):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = one.image.allocate(template, image_datastore)
    wait_until(lambda: one.image.info(image_id).STATE == ImageStates.READY)

    yield image_id

    one.image.delete(image_id)
    wait_until(lambda: image_id not in [image.ID for image in one.imagepool.info().IMAGE])



@pytest.fixture
def vm_with_disk(one: One, image: int, system_datastore: int):
    image_id = image
    template = f"""
        NAME = {get_unic_name()}
        CPU = 1
        MEMORY = 32
        VCPU = 1
        DISK=[IMAGE_ID={image_id}]
    """
    vm_id = one.vm.allocate(template, False)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)

    yield vm_id

    one.vm.recover(vm_id, 3)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)




@pytest.fixture(params=[
    pytest.param("backup_datastore", marks=pytest.mark.skipif( Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")),
    pytest.param("file_datastore",   marks=pytest.mark.skipif( Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only"))
])
def backup_image(one: One, vm_with_disk: int, request):
    backup_ds_id = request.getfixturevalue(request.param)

    run_command_via_ssh(brest_admin_ssh_conn, f"onevm backup {vm_with_disk} -d {backup_ds_id}")

    if Version(BREST_VERSION) < Version("4"):
        time.sleep(120)
    else:
        time.sleep(20)

    backups = [image.ID for image in one.imagepool.info().IMAGE if image.TYPE == 6]
    backup_id = max(backups)
    yield backup_id

    one.image.delete(backup_id)
    wait_until(lambda: backup_id not in [image.ID for image in one.imagepool.info().IMAGE])



# =================================================================================================
# TESTS
# =================================================================================================




def test_backup_image_not_exist(one: One, dummy_datastore: int):
    image_id     = 999999
    datastore_id = dummy_datastore

    with pytest.raises(OneNoExistsException):
        one.image.restore(image_id, datastore_id)




def test_wrong_image_type(one: One, dummy_image: int, dummy_datastore: int):
    image_id     = dummy_image
    datastore_id = dummy_datastore

    assert one.image.info(image_id).TYPE != 6

    with pytest.raises(OneException):
        one.image.restore(image_id, datastore_id)




def test_backup_datastore_not_exist(one: One, backup_image: int):
    image_id     = backup_image
    datastore_id = 99999

    assert one.image.info(image_id).TYPE == 6

    with pytest.raises(OneNoExistsException):
        one.image.restore(image_id, datastore_id)



@pytest.mark.skipif(Version(BREST_VERSION) >= Version("4"), reason="Brest 3.x only")
def test_restore_into_certain_storage_v3(one: One, backup_image: int, dummy_datastore: int):
    image_id     = backup_image
    datastore_id = dummy_datastore

    backup_info = one.image.info(image_id)
    assert backup_info.TYPE == 6

    backuped_vm_id      = int(backup_info.TEMPLATE["ONEVMID"])
    restored_vm_id      = backuped_vm_id + 1
    restored_image_id   = backup_image + 1

    one.image.restore(backup_image, datastore_id)
    wait_until(lambda: one.vm.info(restored_vm_id).STATE == VmStates.POWEROFF)

    assert one.image.info(restored_image_id).DATASTORE_ID == datastore_id

    one.vm.action("terminate-hard", restored_vm_id)
    wait_until(lambda: one.vm.info(restored_vm_id).STATE == VmStates.DONE)

    one.image.delete(restored_image_id)
    wait_until(lambda: restored_image_id not in [image.ID for image in one.imagepool.info().IMAGE])




@pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
def test_restore_without_template(one: One, backup_image: int, dummy_datastore: int):
    image_id             = backup_image
    datastore_id         = dummy_datastore
    backup_info          = one.image.info(image_id)
    vm_id                = backup_info.VMS.ID[-1]
    api_response         = one.image.restore(backup_image, datastore_id)
    ids                  = [int(_id) for _id in api_response.split()]
    restored_template_id = ids[0]
    restored_image_ids   = ids[1:]

    time.sleep(30)

    assert one.template.info(restored_template_id).NAME.startswith(str(vm_id))

    for restored_image_id in restored_image_ids:
        assert one.image.info(restored_image_id).NAME.startswith(str(vm_id))

    one.template.delete(restored_template_id, delete_images=True)

    time.sleep(10)



@pytest.mark.skipif(Version(BREST_VERSION) < Version("4"), reason="Brest 4.x only")
def test_restore_with_template(one: One, backup_image: int, dummy_datastore: int):
    image_id             = backup_image
    datastore_id         = dummy_datastore
    name                 = get_unic_name()
    template             = f"NAME={name}"
    backup_info          = one.image.info(backup_image)
    vm_id                = backup_info.VMS.ID[-1]
    api_response         = one.image.restore(image_id, datastore_id, template)
    ids                  = [int(_id) for _id in api_response.split()]
    restored_template_id = ids[0]
    restored_image_ids   = ids[1:]

    time.sleep(30)

    assert one.template.info(restored_template_id).NAME == name

    for restored_image_id in restored_image_ids:
        assert one.image.info(restored_image_id).NAME.startswith(f"{name}-disk-")

    one.template.delete(restored_template_id, delete_images=True)

    time.sleep(10)