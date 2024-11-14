import pytest

from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template, template_exist
from one_cli.image      import Image, create_image, image_exist
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM

from tests._common_tests.info import info_if_not_exist__test
from tests._common_tests.info import info__test


BRESTADM_AUTH = get_user_auth(BRESTADM)


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



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One):
    info_if_not_exist__test(one.template)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_info(one: One, vmtemplate: Template):
    info__test(one.template, vmtemplate)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_extended_template_info(one: One, vmtemplate_with_image: Template):
    template  = one.template.info(vmtemplate_with_image._id, extended=True).TEMPLATE
    disk_info = template["DISK"] if isinstance(template["DISK"], dict) else template["DISK"][0]
    assert "SIZE" in disk_info
