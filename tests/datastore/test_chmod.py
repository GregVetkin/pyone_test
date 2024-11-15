import pytest
from api                        import One
from utils                      import get_unic_name
from one_cli.datastore          import Datastore, create_datastore
from config                     import ADMIN_NAME
from tests._common_tests.chmod  import chmod__test, chmod_if_not_exist__test, _rights_tuples_list






@pytest.fixture(scope="module")
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



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_not_exist(one: One):
    chmod_if_not_exist__test(one.datastore)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_datastore_rights(one: One, datastore: Datastore, rights):
    chmod__test(one.datastore, datastore, rights)

