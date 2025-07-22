import pytest
import random
from api                        import One
from utils.other                import get_unic_name, wait_until



def images(one: One, dummy_datastore: int):
    datastore_id = dummy_datastore
    image_ids    = []

    for _ in random.randint(2, 5):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = one.image.allocate(template, datastore_id)
        image_ids.append(image_id)
    
    yield image_ids

    for image_id in image_ids:
        one.image.delete(image_id, True)
    
    wait_until(
        lambda: one.datastore.info(datastore_id, False).IMAGES.ID is None
        )



@pytest.fixture
def vmtemplate_with_images():
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
    chmod_if_not_exist__test(one.template)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_template_rights(one: One, vmtemplate: Template, rights):
    chmod__test(one.template, vmtemplate, rights)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_template_rights_and_its_images(one: One, vmtemplate_with_many_images: Template, rights):
    vmtemplate_disks = vmtemplate_with_many_images.info().TEMPLATE["DISK"]
    image_ids = [vmtemplate_disks[i]["IMAGE_ID"] for i, _ in enumerate(vmtemplate_disks)]
    images    = [Image(image_id) for image_id in image_ids]

    one.template.chmod(vmtemplate_with_many_images._id, *rights, chmod_images=True)

    assert _rights_as_tuple(vmtemplate_with_many_images) == rights
    for image in images:
        assert _rights_as_tuple(image) == rights



    

