import pytest
import random
import pyone

from typing                         import List
from api                            import One
from utils.other                    import get_unic_name, wait_until
from tests._common_methods.chmod    import random_chmod__test, not_exist__test



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




def test_change_template_permissions(one: One, dummy_template: int):
    template_id = dummy_template
    random_chmod__test(one.template, template_id)




def test_change_template_permissions_and_its_images(one: One, vmtemplate_with_images: int):
    template_id = vmtemplate_with_images
    image_ids   = [int(disk["IMAGE_ID"]) for disk in one.template.info(template_id, False, False).TEMPLATE["DISK"]]
    permissions = (1, 1, 1, 1, 1, 1, 1, 1, 1)

    _id = one.template.chmod(template_id, *permissions, True)
    assert _id == template_id

    new_template_permissions = one.template.info(template_id, False, False).PERMISSIONS

    assert new_template_permissions.OWNER_U == 1
    assert new_template_permissions.OWNER_M == 1
    assert new_template_permissions.OWNER_A == 1

    assert new_template_permissions.GROUP_U == 1
    assert new_template_permissions.GROUP_M == 1
    assert new_template_permissions.GROUP_A == 1

    assert new_template_permissions.OTHER_U == 1
    assert new_template_permissions.OTHER_M == 1
    assert new_template_permissions.OTHER_A == 1


    for image_id in image_ids:
        new_image_permissions = one.image.info(image_id, False).PERMISSIONS

        assert new_template_permissions.OWNER_U == new_image_permissions.OWNER_U
        assert new_template_permissions.OWNER_M == new_image_permissions.OWNER_M
        assert new_template_permissions.OWNER_A == new_image_permissions.OWNER_A

        assert new_template_permissions.GROUP_U == new_image_permissions.GROUP_U
        assert new_template_permissions.GROUP_M == new_image_permissions.GROUP_M
        assert new_template_permissions.GROUP_A == new_image_permissions.GROUP_A

        assert new_template_permissions.OTHER_U == new_image_permissions.OTHER_U
        assert new_template_permissions.OTHER_M == new_image_permissions.OTHER_M
        assert new_template_permissions.OTHER_A == new_image_permissions.OTHER_A



    

