import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte

from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)
    
    yield image

    image.delete()



@pytest.fixture
def prepare_second_image():
    image_template = """
        NAME = api_test_image_2
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
        one.image.rename(99999, "GregoryVetkin")



def test_change_image_name(prepare_image):
    one      = One(BRESTADM_SESSION)
    image    = prepare_image
    new_name = "api_test_image_new"

    one.image.rename(image._id, new_name)
    assert image.info().NAME == new_name



def test_image_name_collision(prepare_image, prepare_second_image):
    one     = One(BRESTADM_SESSION)
    image_1 = prepare_image
    image_2 = prepare_second_image

    image_1_old_info = image_1.info()
    with pytest.raises(OneActionException):
        one.image.rename(image_1._id, image_2.info().NAME)
    image_1_new_info = image_1.info()

    assert image_1_new_info.NAME == image_1_old_info.NAME



def test_empty_image_name(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    image_old_info = image.info()
    with pytest.raises(OneActionException):
        one.image.rename(image._id, "")
    image_new_info = image.info()

    assert image_old_info.NAME == image_new_info.NAME



def test_unavailable_symbols_in_image_name(prepare_image):
    one             = One(BRESTADM_SESSION)
    image           = prepare_image
    bad_symbols     = ["$", "#", "&", "\"", "\'", ">", "<", "/", "\\", "|"]
    image_old_info  = image.info()

    for symbol in bad_symbols:
        with pytest.raises(OneActionException):
            one.image.rename(image._id, "api_test_image_" + symbol)

        assert image.info().NAME == image_old_info.NAME

