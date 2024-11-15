import pytest
from api                        import One
from utils                      import get_user_auth, get_unic_name
from one_cli.template           import Template, create_template, template_exist
from one_cli.image              import Image, create_image, image_exist
from one_cli.datastore          import Datastore, create_datastore
from config                     import BRESTADM
from tests._common_tests.chmod  import chmod__test, chmod_if_not_exist__test, _rights_tuples_list, _rights_as_tuple


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
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
    

@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def vmtemplate_with_many_images(image: Image, image_2: Image):
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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One):
    chmod_if_not_exist__test(one.template)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_template_rights(one: One, vmtemplate: Template, rights):
    chmod__test(one.template, vmtemplate, rights)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_template_rights_and_its_images(one: One, vmtemplate_with_many_images: Template, rights):
    vmtemplate_disks = vmtemplate_with_many_images.info().TEMPLATE["DISK"]
    image_ids = [vmtemplate_disks[i]["IMAGE_ID"] for i, _ in enumerate(vmtemplate_disks)]
    images    = [Image(image_id) for image_id in image_ids]

    one.template.chmod(vmtemplate_with_many_images._id, *rights, chmod_images=True)

    assert _rights_as_tuple(vmtemplate_with_many_images) == rights
    for image in images:
        assert _rights_as_tuple(image) == rights



    

