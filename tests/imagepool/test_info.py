import pytest

from api            import One
from pyone          import OneServer
from utils          import get_user_auth
from one_cli.image  import Image, create_image_by_tempalte
from config         import API_URI, BRESTADM



BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)



@pytest.fixture
def prepare_images():
    image_list = []
    for _ in range(5):
        template = f"""
            NAME = api_test_image_{_}
            TYPE = DATABLOCK
            SIZE = 10
        """
        image_id = create_image_by_tempalte(1, template, False)
        image    = Image(image_id)
        image_list.append(image)

    yield image_list

    for image in image_list:
        image.delete()




# =================================================================================================
# TESTS
# =================================================================================================



def test_show_all_images(prepare_images):
    one         = One(BRESTADM_SESSION)
    image_ids   = [image.info().ID for image in prepare_images]

    imagepool       = one.imagepool.info().IMAGE
    imagepool_ids   = [image.ID for image in imagepool]
    
    assert set(image_ids).issubset(imagepool_ids)



def test_filter_start_id(prepare_images):
    one         = One(BRESTADM_SESSION)
    image_ids   = [image.info().ID for image in prepare_images]
    image_ids.sort()

    imagepool       = one.imagepool.info(start_id=image_ids[1]).IMAGE
    imagepool_ids   = [image.ID for image in imagepool]
    

    assert image_ids[0] not in imagepool_ids
    assert set(image_ids[1:]).issubset(imagepool_ids)



def test_filter_end_id(prepare_images):
    one         = One(BRESTADM_SESSION)
    image_ids   = [image.info().ID for image in prepare_images]
    image_ids.sort()

    imagepool       = one.imagepool.info(start_id=image_ids[0], end_id=image_ids[-2]).IMAGE
    imagepool_ids   = [image.ID for image in imagepool]
    

    assert image_ids[-1] not in imagepool_ids
    assert set(image_ids[:-2]).issubset(imagepool_ids)

