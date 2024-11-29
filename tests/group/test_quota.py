import pytest
from typing                 import List
from random                 import randint
from api                    import One
from pyone                  import OneException
from utils                  import get_unic_name
from config                 import ADMIN_NAME
from one_cli.group          import Group, group_exist, create_group
from one_cli.group._common  import ImageQuotaInfo, NetworkQuotaInfo, DatastoreQuotaInfo
from one_cli.datastore      import Datastore, create_datastore
from one_cli.image          import Image, create_image
from one_cli.vnet           import Vnet, create_vnet




@pytest.fixture
def group():
    _id     = create_group(get_unic_name())
    group   = Group(_id)
    yield group
    group.delete()


@pytest.fixture(scope="module")
def image_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def images(image_datastore: Datastore):
    image_list = []
    for _ in range(5):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = create_image(image_datastore._id, template, False)
        image    = Image(image_id)
        image_list.append(image)

    yield image_list

    for image in image_list:
        image.delete()


@pytest.fixture
def datastores():
    datastore_list = []
    for _ in range(5):
        template = f"""
            NAME   = {get_unic_name()}
            TYPE   = IMAGE_DS
            TM_MAD = ssh
            DS_MAD = fs
        """
        datastore_id = create_datastore(template)
        datastore    = Datastore(datastore_id)
        datastore_list.append(datastore)

    yield datastore_list

    for datastore in datastore_list:
        datastore.delete()


@pytest.fixture
def vnets():
    vnet_list = []
    for _ in range(5):
        vnet_template = f"""
            NAME   = {get_unic_name()}
            VN_MAD = bridge
        """
        vnet_id = create_vnet(vnet_template)
        vnet    = Vnet(vnet_id)
        vnet_list.append(vnet)

    yield vnet_list

    for vnet in vnet_list:
        vnet.delete()


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One):
    with pytest.raises(OneException):
        one.group.quota(999999, "")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_quota(one: One, group: Group):
    vms                 = randint(1, 1024)
    cpu                 = randint(1, 1024)
    memory              = randint(1, 1024)
    system_disk_size    = randint(1, 1024)
    running_cpu         = randint(1, 1024)
    running_memory      = randint(1, 1024)
    running_vms         = randint(1, 1024)
    
    vm_quota_template   = f"""
        VM=[
            VMS="{vms}",
            CPU="{cpu}",
            MEMORY="{memory}",
            SYSTEM_DISK_SIZE="{system_disk_size}",
            RUNNING_CPU="{running_cpu}",
            RUNNING_MEMORY="{running_memory}",
            RUNNING_VMS="{running_vms}"
        ]
    """
    _id = one.group.quota(group._id, vm_quota_template)
    assert _id == group._id

    group_info = group.info()
    assert group_info.VM_QUOTA
    assert not group_info.DATASTORE_QUOTA
    assert not group_info.IMAGE_QUOTA
    assert not group_info.NETWORK_QUOTA

    assert group_info.VM_QUOTA.VMS              == vms
    assert group_info.VM_QUOTA.CPU              == cpu
    assert group_info.VM_QUOTA.MEMORY           == memory
    assert group_info.VM_QUOTA.SYSTEM_DISK_SIZE == system_disk_size
    assert group_info.VM_QUOTA.RUNNING_CPU      == running_cpu
    assert group_info.VM_QUOTA.RUNNING_MEMORY   == running_memory
    assert group_info.VM_QUOTA.RUNNING_VMS      == running_vms

  



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_storage_quota(one: One, group: Group, datastores: List[Datastore]):
    ds_quotas = {}
    ds_quota_template = ""
    for _ in range(len(datastores)):
        ds_id       = datastores[_]._id
        ds_images   = randint(1, 1024)
        ds_size     = randint(1, 1024)
        ds_quotas[ds_id] = DatastoreQuotaInfo(
                                        ID=          ds_id,
                                        IMAGES=      ds_images,
                                        SIZE=        ds_size,
                                        IMAGES_USED= 0,
                                        SIZE_USED=   0,
                                    )
        ds_quota_template += f"""
            DATASTORE=[
                ID="{ds_id}",
                IMAGES="{ds_images}",
                SIZE="{ds_size}"
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




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_quota(one: One, group: Group, images: List[Image]):
    img_quotas = {}
    img_quota_template = ""
    for _ in range(len(images)):
        img_id    = images[_]._id
        img_rvms  = randint(1, 1024)
        img_quotas[img_id] = ImageQuotaInfo(
                                        ID=         img_id,
                                        RVMS=       img_rvms,
                                        RVMS_USED=  0,
                                    )
        img_quota_template += f"""
            IMAGE=[
                ID="{img_id}",
                RVMS="{img_rvms}"
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



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
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



