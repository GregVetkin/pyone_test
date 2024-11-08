import pytest

from api                import One
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM
from typing             import List


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
def datastores():
    datastore_list = []
    for _ in range(5):
        template = f"""
            NAME   = api_test_ds_{_}
            TYPE   = IMAGE_DS
            TM_MAD = ssh
            DS_MAD = fs
        """
        datastore_id = create_datastore(template)
        datastore    = Datastore(datastore_id)
        datastore_list.append(datastore)

    yield datastore_list

    for datastore in datastore_list:
        datastore.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def test_show_all_datastores(one: One, datastores: List[Datastore]):
    datastore_ids       = [datastore.info().ID for datastore in datastores]
    datastorepool       = one.datastorepool.info().DATASTORE
    datastorepool_ids   = [datastore.ID for datastore in datastorepool]
    
    assert set(datastore_ids).issubset(datastorepool_ids)

