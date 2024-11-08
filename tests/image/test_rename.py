import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = """
        NAME = api_test_image_1
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture
def image_2(datastore: Datastore):
    template = """
        NAME = api_test_image_2
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.rename(99999, "GregoryVetkin")



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_image_name(one: One, image: Image):
    new_name = "api_test_image_new"
    one.image.rename(image._id, new_name)
    image_new_name = image.info().NAME
    assert new_name == image_new_name


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_name_collision(one: One, image: Image, image_2: Image):
    image_old_name = image.info().NAME
    with pytest.raises(OneActionException):
        one.image.rename(image._id, image_2.info().NAME)
    image_new_name = image.info().NAME
    assert image_old_name == image_new_name



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_empty_image_name(one: One, image: Image):
    image_old_name = image.info().NAME
    with pytest.raises(OneActionException):
        one.image.rename(image._id, "")
    image_new_name = image.info().NAME
    assert image_old_name == image_new_name



@pytest.mark.parametrize("bad_symbol", ["$", "#", "&", "\"", "\'", ">", "<", "/", "\\", "|"])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unavailable_symbols_in_image_name(one: One, image: Image, bad_symbol: str):
    image_old_name = image.info().NAME

    with pytest.raises(OneActionException):
        one.image.rename(image._id, f"test{bad_symbol}")
    assert image_old_name == image.info().NAME

    with pytest.raises(OneActionException):
        one.image.rename(image._id, f"{bad_symbol}test")
    assert image_old_name == image.info().NAME

    with pytest.raises(OneActionException):
        one.image.rename(image._id, f"te{bad_symbol}st")
    assert image_old_name == image.info().NAME

    with pytest.raises(OneActionException):
        one.image.rename(image._id, bad_symbol)
    assert image_old_name == image.info().NAME
