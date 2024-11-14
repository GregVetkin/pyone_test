import pytest
from typing             import List
from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
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


@pytest.fixture(scope="module")
def images(datastore: Datastore):
    image_list = []
    for _ in range(5):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = create_image(datastore._id, template, False)
        image    = Image(image_id)
        image_list.append(image)

    yield image_list

    for image in image_list:
        image.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_show_all_images(one: One, images: List[Image]):
    image_ids     = [image._id for image in images]
    imagepool     = one.imagepool.info().IMAGE
    imagepool_ids = [image.ID for image in imagepool]

    assert set(image_ids).issubset(imagepool_ids)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_filter_start_id(one: One, images: List[Image]):
    image_ids     = [image._id for image in images]
    image_ids.sort()
    imagepool     = one.imagepool.info(start_id=image_ids[1]).IMAGE
    imagepool_ids = [image.ID for image in imagepool]
    
    assert image_ids[0] not in imagepool_ids
    assert set(image_ids[1:]).issubset(imagepool_ids)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_filter_end_id(one: One, images: List[Image]):
    image_ids     = [image._id for image in images]
    image_ids.sort()
    imagepool     = one.imagepool.info(start_id=image_ids[0], end_id=image_ids[-2]).IMAGE
    imagepool_ids = [image.ID for image in imagepool]
    
    assert image_ids[-1] not in imagepool_ids
    assert set(image_ids[:-2]).issubset(imagepool_ids)
