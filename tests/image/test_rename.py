import pytest

from api                            import One
from utils.other                    import get_unic_name
from config.tests                   import INVALID_CHARS
from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test






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
    rename__test(one.image, image_id)


def test_name_collision(one: One, dummy_image: int, taken_image_name: str):
    image_id    = dummy_image
    taken_name  = taken_image_name
    cant_be_renamed__test(one.image, image_id, taken_name)



def test_empty_image_name(one: One, dummy_image: int):
    image_id = dummy_image
    cant_be_renamed__test(one.image, image_id, "")


@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_image: int, char: str):
    image_id = dummy_image
    cant_be_renamed__test(one.image, image_id, f"{char}")
    cant_be_renamed__test(one.image, image_id, f"Greg{char}")
    cant_be_renamed__test(one.image, image_id, f"{char}Vetkin")
    cant_be_renamed__test(one.image, image_id, f"Greg{char}Vetkin")