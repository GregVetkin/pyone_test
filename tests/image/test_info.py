import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield image_id

    delete_image(image_id)
    

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
    image_id    = prepare_image
    image_info  = one.image.info(image_id)
    assert image_id == image_info.ID

