import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
def datastore():
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
def user():
    user_id = create_user("api_test_user")
    user    = User(user_id)
    yield user
    user.delete()


@pytest.fixture
def group():
    group_id = create_group("api_test_group")
    group    = Group(group_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.chown(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_user_not_exist(one: One, datastore: Datastore):
    datastore_old_info = datastore.info()
    with pytest.raises(OneNoExistsException):
        one.datastore.chown(datastore._id, user_id=999999)
    datastore_new_info = datastore.info()

    assert datastore_old_info.UID == datastore_new_info.UID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_group_not_exist(one: One, datastore: Datastore):
    datastore_old_info = datastore.info()
    with pytest.raises(OneNoExistsException):
        one.datastore.chown(datastore._id, group_id=999999)
    datastore_new_info = datastore.info()

    assert datastore_old_info.GID == datastore_new_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_user_and_group_change(one: One, datastore: Datastore, user: User, group: Group):
    one.datastore.chown(datastore._id, user._id, group._id)
    datastore_new_info = datastore.info()

    assert user._id  == datastore_new_info.UID
    assert group._id == datastore_new_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_user_and_group_not_changed(one: One, datastore: Datastore):
    datastore_old_info = datastore.info()
    one.datastore.chown(datastore._id)
    datastore_new_info = datastore.info()

    assert datastore_old_info.UNAME == datastore_new_info.UNAME
    assert datastore_old_info.GNAME == datastore_new_info.GNAME



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_user_change(one: One, datastore: Datastore, user: User):
    datastore_old_info = datastore.info()
    one.datastore.chown(datastore._id, user._id)
    datastore_new_info = datastore.info()

    assert datastore_new_info.UID == user._id
    assert datastore_new_info.GID == datastore_old_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_group_change(one: One, datastore: Datastore, group: Group):
    datastore_old_info = datastore.info()
    one.datastore.chown(datastore._id, group_id=group._id)
    datastore_new_info = datastore.info()

    assert datastore_new_info.UID == datastore_old_info.UID
    assert datastore_new_info.GID == group._id

