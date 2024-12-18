import pytest

from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME, LOCK_LEVELS

from tests._common_tests.unlock   import unlock_locked__test
from tests._common_tests.unlock   import unlock_unlocked__test
from tests._common_tests.unlock   import unlock_if_not_exist__test




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


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    unlock_if_not_exist__test(one.image)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_unlocked_image(one: One, image: Image):
    unlock_unlocked__test(one.image, image)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unlock_locked_image(one: One, image: Image, lock_level):
    image.lock(lock_level)
    unlock_locked__test(one.image, image)

