import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, get_image_name

from config             import API_URI


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_name      = "api_test_image"
    image_template  = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield image_id, image_name

    delete_image(image_id)


@pytest.fixture
def prepare_second_image():
    image_name      = "api_test_image_2"
    image_template  = f"""
        NAME = {image_name}
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield image_id, image_name

    delete_image(image_id)



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.rename(99999, "GregoryVetkin")


def test_change_image_name(prepare_image):
    one             = One(BRESTADM_SESSION)
    image_id, _     = prepare_image
    new_image_name  = "api_test_image_new"
    one.image.rename(image_id, new_image_name)
    assert get_image_name(image_id) == new_image_name


def test_image_name_collision(prepare_image, prepare_second_image):
    one                         = One(BRESTADM_SESSION)
    image_1_id, image_1_name    = prepare_image
    _, image_2_name             = prepare_second_image

    with pytest.raises(OneActionException):
        one.image.rename(image_1_id, image_2_name)

    assert get_image_name(image_1_id) == image_1_name


def test_empty_image_name(prepare_image):
    one                  = One(BRESTADM_SESSION)
    image_id, image_name = prepare_image

    with pytest.raises(OneActionException):
        one.image.rename(image_id, "")
        
    assert get_image_name(image_id) == image_name


def test_unavailable_symbols_in_image_name(prepare_image):
    one                     = One(BRESTADM_SESSION)
    image_id, image_name    = prepare_image
    bad_symbols             = ["$", "#", "&", "\"", "\'", ">", "<", "/", "\\", "|"]

    for symbol in bad_symbols:
        new_name = "api_test_image_" + symbol
        with pytest.raises(OneActionException):
            one.image.rename(image_id, new_name)
        assert get_image_name(image_id) == image_name

