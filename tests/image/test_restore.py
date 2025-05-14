import pytest
import time
from api                import One
from pyone              import OneNoExistsException, OneException
from utils              import get_unic_name, run_command
from config             import ADMIN_NAME, BREST_VERSION



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
    time.sleep(3)
    one.datastore.delete(datastore_id)


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
    time.sleep(3)
    one.datastore.delete(datastore_id)


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
    time.sleep(3)
    one.datastore.delete(datastore_id)


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
    time.sleep(3)
    one.datastore.delete(datastore_id)


@pytest.fixture
def image(one: One, image_datastore: int):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = one.image.allocate(template, image_datastore)
    while one.image.info(image_id).STATE != 1: time.sleep(1)
    yield image_id
    time.sleep(3)
    one.image.delete(image_id)



@pytest.fixture
def vm_with_disk(one: One, system_datastore: int, image: int):
    template = f"""
        NAME = {get_unic_name()}
        CPU = 1
        MEMORY = 32
        DISK = [IMAGE_ID={image}]
    """
    vm_id = one.vm.allocate(template)
    time.sleep(5)
    while one.vm.info(vm_id).STATE != 8: time.sleep(1)
    yield vm_id
    one.vm.action("terminate-hard", vm_id)
    while one.vm.info(vm_id).STATE != 6: time.sleep(1)




@pytest.fixture(params=[
    pytest.param("backup_datastore", marks=pytest.mark.skipif(BREST_VERSION < 4 ,   reason="for Brest 4.x")),
    pytest.param("file_datastore",   marks=pytest.mark.skipif(BREST_VERSION > 3,    reason="for Brest 3.x"))
])
def backup_image(one: One, vm_with_disk: int, request):
    backup_ds_id = request.getfixturevalue(request.param)
    run_command(f"sudo onevm backup {vm_with_disk} -d {backup_ds_id}")
    if BREST_VERSION < 4:
        time.sleep(120)
    else:
        time.sleep(20)
    backups = [image.ID for image in one.imagepool.info().IMAGE if image.TYPE == 6]
    backup_id = max(backups)
    yield backup_id
    time.sleep(3)
    one.image.delete(backup_id)




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_backup_image_not_exist(one: One, image_datastore: int):
    with pytest.raises(OneNoExistsException):
        one.image.restore(999999, image_datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_wrong_image_type(one: One, image: int, image_datastore: int):
    assert one.image.info(image).TYPE != 6
    with pytest.raises(OneException):
        one.image.restore(image, image_datastore)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_backup_datastore_not_exist(one: One, backup_image: int):
    assert one.image.info(backup_image).TYPE == 6
    with pytest.raises(OneNoExistsException):
        one.image.restore(backup_image, 999999)



@pytest.mark.skipif(BREST_VERSION > 3, reason="for Brest 3.x")
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_restore_into_certain_storage_v3(one: One, backup_image: int, image_datastore: int):
    backup_info = one.image.info(backup_image)
    assert backup_info.TYPE == 6

    backuped_vm_id      = int(backup_info.TEMPLATE["ONEVMID"])
    restored_vm_id      = backuped_vm_id + 1
    restored_image_id   = backup_image + 1

    one.image.restore(backup_image, image_datastore)
    time.sleep(30)

    assert image_datastore == one.image.info(restored_image_id).DATASTORE_ID
    assert one.vm.info(restored_vm_id)

    one.vm.action("terminate-hard", restored_vm_id)
    while one.vm.info(restored_vm_id).STATE != 6: time.sleep(1)
    one.image.delete(restored_image_id)
    time.sleep(5)




@pytest.mark.skipif(BREST_VERSION < 4, reason="for Brest 4.x")
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_restore_without_template_v4(one: One, backup_image: int, image_datastore: int):
    backup_image_info    = one.image.info(backup_image)
    vm_id                = backup_image_info.VMS.ID[-1]
    answer               = one.image.restore(backup_image, image_datastore)
    ids                  = [int(_id) for _id in answer.split()]
    restored_template_id = ids[0]
    restored_image_ids   = ids[1:]

    time.sleep(30)

    assert one.template.info(restored_template_id).NAME.startswith(str(vm_id))

    for restored_image_id in restored_image_ids:
        assert one.image.info(restored_image_id).NAME.startswith(str(vm_id))

    one.template.delete(restored_template_id, delete_images=True)