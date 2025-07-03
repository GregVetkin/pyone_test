import pytest

from api                            import One
from tests._common_methods.info     import info_if_not_exist__test
from tests._common_methods.info     import info__test






def test_image_not_exist(one: One):
    info_if_not_exist__test(one.image)



def test_image_info(one: One, dummy_image: int):
    image_id = dummy_image
    info__test(one.image, image_id)
