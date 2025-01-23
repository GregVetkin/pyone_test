import pytest
import random


from time               import sleep
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image
from one_cli.vm         import VirtualMachine
from config             import ADMIN_NAME


def await_vm_status_code(one: One, vm_id: int, status_code: int, intervals=1.0):
    while one.vm.info(vm_id).STATE != status_code:
        sleep(intervals)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    ds_id = 1
    for ds in one.datastorepool.info().DATASTORE:
        if ds.NAME.startswith("image_"):
            ds_id = ds.ID
            break

    _id = one.image.allocate(template, ds_id, False)

    yield Image(_id)

    while one.image.info(_id).STATE != 1:
        sleep(1)

    one.image.delete(_id, True)



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n")
    await_vm_status_code(one, vm_id, 8)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)
    await_vm_status_code(one, vm_id, 6)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm_with_disk(one: One, image: Image, vm: VirtualMachine): 
    one.vm.attach(vm._id, f"DISK=[IMAGE_ID={image._id}]")
    await_vm_status_code(one, vm._id, 8)

    yield VirtualMachine(vm._id)

    one.vm.detach(vm._id, 0)
    await_vm_status_code(one, vm._id, 8)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm_with_disk_snapshots(one: One, image: Image, vm: VirtualMachine):

    for disk_number in range(random.randint(2, 5)):
        one.vm.attach(vm._id, f"DISK=[IMAGE_ID={image._id}]")
        await_vm_status_code(one, vm._id, 8)
        for _ in range(random.randint(2, 4)):
            one.vm.disksnapshotcreate(vm._id, disk_number, get_unic_name())
            await_vm_status_code(one, vm._id, 8)
    
    yield VirtualMachine(vm._id)

    for disk_info in one.vm.info(vm._id).TEMPLATE["DISK"]:
        disk_id = int(disk_info["DISK_ID"])
        one.vm.detach(vm._id, disk_id)
        await_vm_status_code(one, vm._id, 8)
    

    



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    vm_id       = 99999
    disk_id     = 0
    snapshot_id = 0

    with pytest.raises(OneException):
        one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disk_not_exist(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 99999
    snapshot_id = 0

    with pytest.raises(OneException):
        one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_disksnapshot_not_exist(one: One, vm_with_disk: VirtualMachine):
    vm_id       = vm_with_disk._id
    disk_id     = 0
    snapshot_id = 99999

    with pytest.raises(OneException):
        one.vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)
    



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_disk_snapshot(one: One, vm_with_disk_snapshots: VirtualMachine):
    vm_id = vm_with_disk_snapshots._id


    disks_snapshots_before = {disk_snapshots_info.DISK_ID : [snapshot_info.ID for snapshot_info in disk_snapshots_info.SNAPSHOT]
                            for disk_snapshots_info in one.vm.info(vm_id).SNAPSHOTS}
    snapshots_count_before = sum(len(disks_snapshots_before[disk_id]) for disk_id in disks_snapshots_before)

    assert snapshots_count_before > 0, "VM doesnt have disks with snapshots"

    # нужно исключить ситуацию, когда id объектов совпадают - иначе проверка возвращаемого id удаленного снэпшота бессмысленна
    while True:
        target_disk_id      = random.choice(list(disks_snapshots_before.keys()))
        target_snapshot_id  = random.choice(disks_snapshots_before[target_disk_id])
        if (target_disk_id != vm_id) and (target_snapshot_id != target_disk_id): break

    deleted_snapshot_id = one.vm.disksnapshotdelete(vm_id, target_disk_id, target_snapshot_id)
    sleep(5)
    
    disks_snapshots_after = {disk_snapshots_info.DISK_ID : [snapshot_info.ID for snapshot_info in disk_snapshots_info.SNAPSHOT]
                            for disk_snapshots_info in one.vm.info(vm_id).SNAPSHOTS}
    snapshots_count_after = sum(len(disks_snapshots_after[disk_id]) for disk_id in disks_snapshots_after)

    assert target_snapshot_id == deleted_snapshot_id
    assert deleted_snapshot_id not in disks_snapshots_after[target_disk_id]
    assert (snapshots_count_before - snapshots_count_after) == 1
    
    
