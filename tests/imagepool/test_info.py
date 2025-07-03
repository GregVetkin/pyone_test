import pytest
from typing             import List
from api                import One
from utils.other        import get_unic_name



@pytest.fixture
def images(one: One, dummy_datastore: int):
    datastore_id = dummy_datastore

    image_ids = []
    for _ in range(5):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = one.image.allocate(template, datastore_id, True)
        image_ids.append(image_id)

    yield image_ids

    for image_id in image_ids:
        one.image.delete(image_id, True)




# =================================================================================================
# TESTS
# =================================================================================================




def test_show_all_images(one: One, images: List[int]):
    image_ids     = images
    imagepool     = one.imagepool.info().IMAGE
    imagepool_ids = [image.ID for image in imagepool]

    assert set(image_ids).issubset(imagepool_ids)




def test_filter_start_id(one: One, images: List[int]):
    image_ids     = images
    image_ids.sort()
    imagepool     = one.imagepool.info(start_id=image_ids[1]).IMAGE
    imagepool_ids = [image.ID for image in imagepool]
    
    assert image_ids[0] not in imagepool_ids
    assert set(image_ids[1:]).issubset(imagepool_ids)




def test_filter_end_id(one: One, images: List[int]):
    image_ids     = images
    image_ids.sort()
    imagepool     = one.imagepool.info(start_id=image_ids[0], end_id=image_ids[-2]).IMAGE
    imagepool_ids = [image.ID for image in imagepool]
    
    assert image_ids[-1] not in imagepool_ids
    assert set(image_ids[:-2]).issubset(imagepool_ids)

