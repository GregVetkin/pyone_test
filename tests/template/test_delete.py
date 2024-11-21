import pytest
from pyone              import OneActionException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image, image_exist
from one_cli.datastore  import Datastore, create_datastore 
from one_cli.template   import Template, create_template, template_exist
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import delete_undeletable__test





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
    if not template_exist(_id):
        return
    if the_template.info().LOCK is not None:
        the_template.unlock()
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
def vmtemplate_with_image(image: Image):
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
        DISK    = [IMAGE_ID = {image._id}]
    """
    _id = create_template(template)
    the_template = Template(_id)

    yield the_template
    
    if not template_exist(_id):
        return
    
    if the_template.info().LOCK is not None:
        the_template.unlock()

    the_template.delete()


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
def vmtemplate_with_2_images(image: Image, image_2: Image):
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
def test_image_not_exist(one: One):
    delete_if_not_exist__test(one.template)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_delete(one: One, vmtemplate: Template):
    delete__test(one.template, vmtemplate)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_locked_template(one: One, vmtemplate: Template, lock_level: int):
    vmtemplate.lock(lock_level)

    if lock_level == 3:
        delete__test(one.template, vmtemplate)
    else:
        delete_undeletable__test(one.template, vmtemplate)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_template_with_image(one: One, vmtemplate_with_image: Template, image: Image):
    one.template.delete(vmtemplate_with_image._id, delete_images=True)
    assert not template_exist(vmtemplate_with_image._id)
    assert not image_exist(image._id)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_template_with_many_images(one: One, vmtemplate_with_2_images: Template):
    vmtemplate_tempalte = vmtemplate_with_2_images.info().TEMPLATE
    assert "DISK" in vmtemplate_tempalte
    template_disks = vmtemplate_tempalte["DISK"]
    assert len(template_disks) > 1

    one.template.delete(vmtemplate_with_2_images._id, delete_images=True)
    assert not template_exist(vmtemplate_with_2_images._id)
    for disk in template_disks:
        assert not image_exist(disk["IMAGE_ID"])


