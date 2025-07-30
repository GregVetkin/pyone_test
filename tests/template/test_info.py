import pytest
import random

from typing         import List
from api            import One
from utils.other    import get_unic_name, wait_until

from tests._common_methods.info     import info__test, not_exist__test





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
        image_id = one.image.allocate(template, datastore_id, False)
        image_ids.append(image_id)
    
    yield image_ids

    for image_id in image_ids:
        one.image.delete(image_id, True)
    
    deleted_ids_set = set(image_ids)

    wait_until(
        lambda: deleted_ids_set.isdisjoint(set(one.datastore.info(datastore_id, False).IMAGES.ID)),
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




def test_template_info(one: One, dummy_template: int):
    template_id = dummy_template
    info__test(one.template, template_id)



@pytest.mark.parametrize("extended", [True, False])
def test_extended_info_with_images(one: One, vmtemplate_with_images: int, extended: bool):
    template_id   = vmtemplate_with_images
    tempalte_info = one.template.info(template_id, extended, True)


    for disk in tempalte_info.TEMPLATE["DISK"]:
        assert "IMAGE_ID" in disk
        
        if extended:
            assert "SIZE" in disk
        else:
            assert "SIZE" not in disk
