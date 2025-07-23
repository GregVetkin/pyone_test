import pytest
import random

from api                            import One
from typing                         import List

from utils.other                    import wait_until
from utils.other                    import get_unic_name

from tests._common_methods.clone    import not_exist__test
from tests._common_methods.clone    import name_collision__test


    

@pytest.fixture
def images(one: One, dummy_datastore: int):
    datastore_id = dummy_datastore
    image_ids    = []

    for _ in range(random.randint(2, 5)):
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
    
    deleted_ids_set = set(image_ids)

    wait_until(
        lambda: deleted_ids_set.isdisjoint(set([image.ID for image in one.imagepool.info().IMAGE])),
        timeout_message="Some images were not removed when the test was completed."
        )



@pytest.fixture
def vmtemplate_with_images(one: One, images: List[int]):
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    for image_id in images:
        template += f"DISK=[IMAGE_ID={image_id}]\n"

    tempalte_id = one.template.allocate(template)

    yield tempalte_id
    
    one.template.delete(tempalte_id, False)







# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    not_exist__test(one.template)
    



def test_name_collisison(one: One, dummy_template: int):
    template_id = dummy_template
    clone_name  = one.template.info(template_id).NAME
    name_collision__test(one.template, template_id, clone_name)
    



def test_clone(one: One, dummy_template: int):
    template_id = dummy_template
    clone_name  = get_unic_name()

    clone_id    = one.template.clone(template_id, clone_name, False)
    wait_until(
        lambda: clone_id in [template.ID for template in one.templatepool.info().VMTEMPLATE],
        timeout_message=f"""The timeout for creating a template clone has expired. Clone template id: {clone_id}"""
        )
    assert one.template.info(clone_id).NAME == clone_name

    one.template.delete(clone_id)

    


@pytest.mark.parametrize("clone_disks", [True, False])
def test_clone_template_with_disks(one: One, vmtemplate_with_images: int, clone_disks: bool):
    template_id         = vmtemplate_with_images
    clone_name          = get_unic_name()
    images_count_before = len(one.imagepool.info().IMAGE)
    template_image_ids  = [int(disk["IMAGE_ID"]) for disk in one.template.info(template_id).TEMPLATE["DISK"]]
    clone_id            = one.template.clone(template_id, clone_name, clone_disks)

    wait_until(
        lambda: clone_id in [template.ID for template in one.templatepool.info().VMTEMPLATE],
        timeout_message=f"""The timeout for creating a template clone has expired. Clone template id: {clone_id}"""
        )
    clone_info          = one.template.info(clone_id)
    clone_image_ids     = [int(disk["IMAGE_ID"]) for disk in one.template.info(clone_id).TEMPLATE["DISK"]]

    assert clone_info.NAME == clone_name

    if clone_disks:
        assert len(template_image_ids) == len(clone_image_ids),       "The number of disks in the template clone differs"
        assert max(template_image_ids) < min(clone_image_ids),        "New images must have an id greater than the original template"
        assert not set(template_image_ids) & set(clone_image_ids),    "The clone template contains old template disks"
        assert images_count_before + len(template_image_ids) ==  len(one.imagepool.info().IMAGE)

        one.template.delete(clone_id, True)
        wait_until(
            lambda: set(clone_image_ids).isdisjoint(set([image.ID for image in one.imagepool.info().IMAGE])),
            timeout_message="Some images were not removed when the test was completed."
        )
    
    else:
        assert set(template_image_ids) == set(clone_image_ids)
        assert images_count_before == len(one.imagepool.info().IMAGE)
        one.template.delete(clone_id, False)