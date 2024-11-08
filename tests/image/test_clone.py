import pytest

from api                import One
from pyone              import OneActionException, OneNoExistsException, OneException
from utils              import get_user_auth
from commands.user      import get_user_id_by_name
from one_cli.image      import create_image_by_tempalte, Image
from one_cli.datastore  import create_ds_by_tempalte, Datastore
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_image_ds_1
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def datastore_2():
    datastore_template = """
        NAME   = api_test_image_ds_2
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def system_datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
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



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.clone(999999, "GregVetkin")



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One, image: Image):
    with pytest.raises(OneNoExistsException):
        one.image.clone(image._id, "GregVetkin", 999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_name_is_taken(one: One, image: Image):
    brestadm_id = get_user_id_by_name("brestadm")
    if image.info().UID != brestadm_id:
        image.chown(brestadm_id)

    with pytest.raises(OneException):
        one.image.clone(image._id, image.info().NAME)
    


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_only_same_datastore_support(one: One, image: Image, system_datastore: Datastore):
    with pytest.raises(OneActionException):
        one.image.clone(image._id, "GregVetkin", system_datastore._id)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_clone_into_the_same_datastore(one: One, image: Image):
    clone_id = one.image.clone(image._id, "GregVetkin")
    clone    = Image(clone_id)
    assert clone.info().DATASTORE_ID == image.info().DATASTORE_ID
    clone.delete()



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_clone_into_another_datastore(one: One, image: Image, datastore_2: Datastore):
    clone_id = one.image.clone(image._id, "GregVetkin", datastore_2._id)
    clone    = Image(clone_id)
    assert clone.info().DATASTORE_ID == datastore_2._id
    clone.delete()
