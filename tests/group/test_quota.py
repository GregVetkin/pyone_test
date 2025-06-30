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
    group_id = dummy_group

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
    assert not group_info.DATASTORE_QUOTA.DATASTORE
    assert not group_info.IMAGE_QUOTA.IMAGE
    assert not group_info.NETWORK_QUOTA.NETWORK

    assert group_info.VM_QUOTA.VM.VMS               == vms
    assert group_info.VM_QUOTA.VM.CPU               == cpu
    assert group_info.VM_QUOTA.VM.MEMORY            == memory
    assert group_info.VM_QUOTA.VM.SYSTEM_DISK_SIZE  == system_disk_size
    assert group_info.VM_QUOTA.VM.RUNNING_CPU       == running_cpu
    assert group_info.VM_QUOTA.VM.RUNNING_MEMORY    == running_memory
    assert group_info.VM_QUOTA.VM.RUNNING_VMS       == running_vms

  




def test_storage_quota(one: One, dummy_group: int, datastores: List[int]):
    ds_quotas = {}
    ds_quota_template = ""
    for _ in range(len(datastores)):
        _id       = datastores[_]._id
        _images   = randint(1, 1024)
        _size     = randint(1, 1024)
        ds_quotas[_id] = DatastoreQuotaInfo(
                                        ID=          _id,
                                        IMAGES=      _images,
                                        SIZE=        _size,
                                        IMAGES_USED= 0,
                                        SIZE_USED=   0,
                                    )
        ds_quota_template += f"""
            DATASTORE=[
                ID=     "{_id}",
                IMAGES= "{_images}",
                SIZE=   "{_size}"
        ]
        """
    
    _id = one.group.quota(group._id, ds_quota_template)
    assert _id == group._id

    group_info = group.info()
    assert group_info.DATASTORE_QUOTA
    assert not group_info.VM_QUOTA
    assert not group_info.IMAGE_QUOTA
    assert not group_info.NETWORK_QUOTA

    for ds_quota in group_info.DATASTORE_QUOTA:
        assert ds_quotas[ds_quota.ID] == ds_quota





def test_image_quota(one: One, group: Group, images: List[Image]):
    img_quotas = {}
    img_quota_template = ""
    for _ in range(len(images)):
        _id   = images[_]._id
        _rvms = randint(1, 1024)
        img_quotas[_id] = ImageQuotaInfo(
                                        ID=         _id,
                                        RVMS=       _rvms,
                                        RVMS_USED=  0,
                                    )
        img_quota_template += f"""
            IMAGE=[
                ID=     "{_id}",
                RVMS=   "{_rvms}"
            ]
        """
    
    _id = one.group.quota(group._id, img_quota_template)
    assert _id == group._id

    group_info = group.info()
    assert  group_info.IMAGE_QUOTA
    assert not group_info.DATASTORE_QUOTA
    assert not group_info.VM_QUOTA
    assert not group_info.NETWORK_QUOTA

    for img_quota in group_info.IMAGE_QUOTA:
        assert img_quotas[img_quota.ID] == img_quota




def test_network_quota(one: One, group: Group, vnets: List[Vnet]):
    vnet_quotas = {}
    vnet_quota_template = ""
    for _ in range(len(vnets)):
        _id     = vnets[_]._id
        _leases = randint(1, 1024)
        vnet_quotas[_id] = NetworkQuotaInfo(
                                        ID=          _id,
                                        LEASES=      _leases,
                                        LEASES_USED= 0,
                                    )
        vnet_quota_template += f"""
            NETWORK=[
                ID=     "{_id}",
                LEASES= "{_leases}"
            ]
        """
    
    _id = one.group.quota(group._id, vnet_quota_template)
    assert _id == group._id

    group_info = group.info()
    assert  group_info.NETWORK_QUOTA
    assert not group_info.IMAGE_QUOTA
    assert not group_info.DATASTORE_QUOTA
    assert not group_info.VM_QUOTA


    for vnet_quota in group_info.NETWORK_QUOTA:
        assert vnet_quotas[vnet_quota.ID] == vnet_quota



