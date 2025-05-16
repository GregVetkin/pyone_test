import pytest

from api                import One
from utils              import get_unic_name
from one_cli.template   import Template, create_template, template_exist
from one_cli.image      import Image, create_image, image_exist
from one_cli.datastore  import Datastore, create_datastore
from one_cli.user       import get_user_id_by_name
from config             import ADMIN_NAME

from tests._common_tests.clone import clone_if_not_exist__test
from tests._common_tests.clone import clone_name_collision__test


@pytest.fixture
def vmtemplate():
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    _id = create_template(template)
    the_template = Template(_id)
    yield the_template
    the_template.delete()
    
@pytest.fixture(scope="module")
def datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    if not image_exist(image_id):
        return
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()
    

@pytest.fixture
def image_2(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    if not image_exist(image_id):
        return
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()


@pytest.fixture
def vmtemplate_with_images(image: Image, image_2: Image):
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
        DISK    = [IMAGE_ID = {image._id}]
        DISK    = [IMAGE_ID = {image_2._id}]
    """
    _id = create_template(template)
    the_template = Template(_id)

    yield the_template
    
    if not template_exist(_id):
        return
    
    if the_template.info().LOCK is not None:
        the_template.unlock()

    the_template.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    clone_if_not_exist__test(one.template)
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_clone_name_collisison(one: One, vmtemplate: Template):
    vmtemplate.chown(user_id=get_user_id_by_name(ADMIN_NAME))
    clone_name_collision__test(one.template, vmtemplate)
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_clone(one: One, vmtemplate: Template):
    _id = one.template.clone(vmtemplate._id, get_unic_name())
    assert template_exist(_id)
    Template(_id).delete()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_clone_template_dont_clone_disks(one: One, vmtemplate_with_images: Template):
    original_disk_ids   = [_["IMAGE_ID"] for _ in vmtemplate_with_images.info().TEMPLATE["DISK"]]
    clone_id            = one.template.clone(vmtemplate_with_images._id, get_unic_name(), False)
    clone               = Template(clone_id)
    clone_disk_ids      = [_["IMAGE_ID"] for _ in clone.info().TEMPLATE["DISK"]]
    
    assert template_exist(clone_id)
    assert clone_disk_ids == original_disk_ids
    clone.delete()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_clone_template_do_clone_disks(one: One, vmtemplate_with_images: Template):
    original            = vmtemplate_with_images
    original_disk_ids   = [_["IMAGE_ID"] for _ in original.info().TEMPLATE["DISK"]]
    clone_id            = one.template.clone(original._id, get_unic_name(), True)
    clone               = Template(clone_id)
    clone_disk_ids      = [_["IMAGE_ID"] for _ in clone.info().TEMPLATE["DISK"]]
    
    assert template_exist(clone_id)
    assert clone_disk_ids != original_disk_ids
    
    for disk_id in clone_disk_ids:
        assert image_exist(disk_id)
        Image(disk_id).delete()
    clone.delete()