import pytest
import pyone

from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test, not_exist__test







@pytest.fixture
def taken_image_name(one: One, dummy_datastore: int):
    datastore_id    = dummy_datastore
    check_capacity  = False
    image_name      = get_unic_name()
    template        = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = one.image.allocate(template, datastore_id, check_capacity)

    yield image_name
    one.image.delete(image_id, force=True)



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    not_exist__test(one.image)



def test_rename_image(one: One, dummy_image: int):
    image_id = dummy_image
    new_name = get_unic_name()
    rename__test(one.image, image_id, new_name)


def test_name_is_taken(one: One, dummy_image: int, taken_image_name: str):
    image_id = dummy_image
    new_name = taken_image_name

    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, new_name)



def test_empty_image_name(one: One, dummy_image: int):
    image_id = dummy_image
    new_name = ""
    
    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_image: int, char: str):
    image_id = dummy_image

    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, f"{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, f"Greg{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, f"{char}Vetkin")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.image, image_id, f"Greg{char}Vetkin")