import pytest

from api                import One
from utils              import get_unic_name
from one_cli.datastore  import Datastore, create_datastore
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import ADMIN_NAME

from tests._common_tests.chown  import chown_object_not_exist__test
from tests._common_tests.chown  import chown_user_not_exist__test
from tests._common_tests.chown  import chown_group_not_exist__test
from tests._common_tests.chown  import chown_user_and_group_change__test
from tests._common_tests.chown  import chown_user_and_group_not_changed__test
from tests._common_tests.chown  import chown_user_change__test
from tests._common_tests.chown  import chown_group_change__test





@pytest.fixture
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()
    
    
@pytest.fixture
def user():
    user_id = create_user(get_unic_name())
    user    = User(user_id)
    yield user
    user.delete()


@pytest.fixture
def group():
    group_id = create_group(get_unic_name())
    group    = Group(group_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    chown_object_not_exist__test(one.datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_exist(one: One, datastore: Datastore):
    chown_user_not_exist__test(one.datastore, datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One, datastore: Datastore):
    chown_group_not_exist__test(one.datastore, datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_user_and_group_change(one: One, datastore: Datastore, user: User, group: Group):
    chown_user_and_group_change__test(one.datastore, datastore, user, group)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_user_and_group_not_changed(one: One, datastore: Datastore):
    chown_user_and_group_not_changed__test(one.datastore, datastore)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_user_change(one: One, datastore: Datastore, user: User):
    chown_user_change__test(one.datastore, datastore, user)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_group_change(one: One, datastore: Datastore, group: Group):
    chown_group_change__test(one.datastore, datastore, group)

