import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)
    
    yield image

    image.delete()
    

# =================================================================================================
# TESTS
# =================================================================================================


def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.info(999999)



def test_image_info(prepare_image):
    """
    TODO:
    -   Add more assertions (probably after creating Image-dataclass) (best to check every param)
    -   What should be decrypted here?
    """
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    image_info  = one.image.info(image._id)
    
    assert image._id == image_info.ID

