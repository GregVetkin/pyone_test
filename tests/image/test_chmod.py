import pytest
from api                        import One
from utils                      import get_unic_name
from one_cli.image              import Image, create_image
from one_cli.datastore          import Datastore, create_datastore
from config                     import ADMIN_NAME, LOCK_LEVELS
from tests._common_tests.chmod  import chmod__test, chmod_if_not_exist__test, _rights_tuples_list, chmod_cant_be_changed__test





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
    image_template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, image_template)
    image    = Image(image_id)
    yield image
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One):
    chmod_if_not_exist__test(one.image)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_image_rights(one: One, image: Image, rights):
    chmod__test(one.image, image, rights)



@pytest.mark.skip(reason="Требует уточнения")
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_locked_image_rights(one: One, image: Image, lock_level):
    image.lock(lock_level)
    chmod_cant_be_changed__test(one.image, image, (0,0,0,0,0,0,0,0,0))

