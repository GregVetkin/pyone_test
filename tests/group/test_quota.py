import pytest
from typing                 import List
from random                 import randint
from api                    import One
from pyone                  import OneNoExistsException, OneInternalException, OneActionException
from utils.other            import get_unic_name





@pytest.fixture
def images(one: One, dummy_datastore: int):
    image_datastore_id  = dummy_datastore
    image_ids_list      = []

    for _ in range(5):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = one.image.allocate(template, image_datastore_id, False)
        image_ids_list.append(image_id)

    yield image_ids_list

    for image_id in image_ids_list:
        one.image.delete(image_id)



@pytest.fixture
def datastores(one: One):
    datastore_ids_list = []

    for _ in range(5):
        template = f"""
            NAME   = {get_unic_name()}
            TYPE   = IMAGE_DS
            TM_MAD = ssh
            DS_MAD = fs
        """
        datastore_id = one.datastore.allocate(template, -1)
        datastore_ids_list.append(datastore_id)

    yield datastore_ids_list

    for datastore_id in datastore_ids_list:
        one.datastore.delete(datastore_id)



@pytest.fixture
def vnets(one: One):
    vnet_ids_list = []
    for _ in range(5):
        vnet_template = f"""
            NAME   = {get_unic_name()}
            VN_MAD = bridge
        """
        vnet_id = one.vn.allocate(vnet_template, -1)
        vnet_ids_list.append(vnet_id)

    yield vnet_ids_list

    for vnet_id in vnet_ids_list:
        one.vn.delete(vnet_id)


# =================================================================================================
# TESTS
# =================================================================================================



def test_group_not_exist(one: One):
    group_id = 99999
    template = ""

    with pytest.raises(OneNoExistsException):
        one.group.quota(group_id, template)



def test_vm_quota(one: One, dummy_group: int):
    group_id            = dummy_group
    vms                 = randint(1, 1024)
    cpu                 = randint(1, 1024)
    memory              = randint(1, 1024)
    system_disk_size    = randint(1, 1024)
    running_cpu         = randint(1, 1024)
    running_memory      = randint(1, 1024)
    running_vms         = randint(1, 1024)
    vm_quota_template   = f"""
        VM=[
            VMS=                "{vms}",
            CPU=                "{cpu}",
            MEMORY=             "{memory}",
            SYSTEM_DISK_SIZE=   "{system_disk_size}",
            RUNNING_CPU=        "{running_cpu}",
            RUNNING_MEMORY=     "{running_memory}",
            RUNNING_VMS=        "{running_vms}"
        ]
    """

    _id = one.group.quota(group_id, vm_quota_template)
    assert _id == group_id

    group_info = one.group.info(group_id)

    assert group_info.VM_QUOTA.VM
    assert group_info.VM_QUOTA.VM.VMS               == vms
    assert group_info.VM_QUOTA.VM.CPU               == cpu
    assert group_info.VM_QUOTA.VM.MEMORY            == memory
    assert group_info.VM_QUOTA.VM.SYSTEM_DISK_SIZE  == system_disk_size
    assert group_info.VM_QUOTA.VM.RUNNING_CPU       == running_cpu
    assert group_info.VM_QUOTA.VM.RUNNING_MEMORY    == running_memory
    assert group_info.VM_QUOTA.VM.RUNNING_VMS       == running_vms

    assert not group_info.DATASTORE_QUOTA.DATASTORE
    assert not group_info.IMAGE_QUOTA.IMAGE
    assert not group_info.NETWORK_QUOTA.NETWORK






def test_storage_quota(one: One, dummy_group: int, dummy_datastore: int):
    group_id        = dummy_group
    datastore_id    = dummy_datastore
    images          = randint(1, 1024)
    size            = randint(1, 1024)
    quota_template  = f"""
        DATASTORE=[
            ID=     "{datastore_id}",
            IMAGES= "{images}",
            SIZE=   "{size}"
        ]
    """
    
    _id = one.group.quota(group_id, quota_template)
    assert _id == group_id

    group_info = one.group.info(group_id)
    
    assert group_info.DATASTORE_QUOTA.DATASTORE
    assert group_info.DATASTORE_QUOTA.DATASTORE[-1].ID      == str(datastore_id)
    assert group_info.DATASTORE_QUOTA.DATASTORE[-1].IMAGES  == str(images)
    assert group_info.DATASTORE_QUOTA.DATASTORE[-1].SIZE    == str(size)

    assert not group_info.VM_QUOTA.VM
    assert not group_info.IMAGE_QUOTA.IMAGE
    assert not group_info.NETWORK_QUOTA.NETWORK



def test_image_quota(one: One, dummy_group: int, dummy_image: int):
    group_id        = dummy_group
    image_id        = dummy_image
    rvms            = randint(1, 1024)
    quota_template  = f"""
        IMAGE=[
            ID=     "{image_id}",
            RVMS=   "{rvms}"
            ]
        """
    
    _id = one.group.quota(group_id, quota_template)
    assert _id == group_id

    group_info = one.group.info(group_id)

    assert group_info.IMAGE_QUOTA.IMAGE
    assert group_info.IMAGE_QUOTA.IMAGE[-1].ID   == str(image_id)
    assert group_info.IMAGE_QUOTA.IMAGE[-1].RVMS == str(rvms)

    assert not group_info.VM_QUOTA.VM
    assert not group_info.NETWORK_QUOTA.NETWORK
    assert not group_info.DATASTORE_QUOTA.DATASTORE






def test_network_quota(one: One, dummy_group: int, dummy_vnet: int):
    group_id        = dummy_group
    vnet_id         = dummy_vnet
    leases          = randint(1, 1024)
    quota_template  = f"""
        NETWORK=[
            ID=     "{vnet_id}",
            LEASES= "{leases}"
        ]
    """
    
    _id = one.group.quota(group_id, quota_template)
    assert _id == group_id

    group_info = one.group.info(group_id)
    assert group_info.NETWORK_QUOTA.NETWORK
    assert group_info.NETWORK_QUOTA.NETWORK[-1].ID      == str(vnet_id)
    assert group_info.NETWORK_QUOTA.NETWORK[-1].LEASES  == str(leases)
    assert not group_info.VM_QUOTA.VM
    assert not group_info.IMAGE_QUOTA.IMAGE
    assert not group_info.DATASTORE_QUOTA.DATASTORE
    



