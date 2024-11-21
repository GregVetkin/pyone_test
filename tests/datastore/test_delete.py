import pytest
import time

from api                import One
from utils              import get_unic_name
from one_cli.datastore  import Datastore, create_datastore, datastore_exist
from one_cli.image      import Image, create_image, image_exist
from config             import ADMIN_NAME

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test




@pytest.fixture
def empty_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore

    if datastore_exist(datastore._id):
        datastore.delete()


@pytest.fixture
def not_empty_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)

    image_template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, image_template, True)
    image    = Image(image_id)

    yield datastore

    if not datastore_exist(datastore._id):
        return
    image.delete()
    while image_exist(image._id):
        time.sleep(2)
    datastore.delete()




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    delete_if_not_exist__test(one.datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_empty_datastore(one: One, empty_datastore: Datastore):
    delete__test(one.datastore, empty_datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_not_empty_datastore(one: One, not_empty_datastore: Datastore):
    cant_be_deleted__test(one.datastore, not_empty_datastore)

