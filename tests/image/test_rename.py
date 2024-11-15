import pytest

from api                        import One
from utils                      import get_unic_name
from one_cli.image              import Image, create_image
from one_cli.datastore          import Datastore, create_datastore
from config                     import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import rename_unavailable_symbol__test
from tests._common_tests.rename import rename_empty_name__test
from tests._common_tests.rename import rename_collision__test




@pytest.fixture(scope="module")
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()


@pytest.fixture
def image_2(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    rename_if_not_exist__test(one.image)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_image_name(one: One, image: Image):
    rename__test(one.image, image)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_name_collision(one: One, image: Image, image_2: Image):
    rename_collision__test(one.image, image, image_2)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_image_name(one: One, image: Image):
    rename_empty_name__test(one.image, image)


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_image_name(one: One, image: Image, bad_symbol: str):
    rename_unavailable_symbol__test(one.image, image, bad_symbol)
