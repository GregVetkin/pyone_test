import pytest

from api                import One
from utils              import get_unic_name
from one_cli.datastore  import Datastore, create_datastore
from config             import ADMIN_NAME
from typing             import List






@pytest.fixture
def datastores():
    datastore_list = []
    for _ in range(5):
        template = f"""
            NAME   = {get_unic_name()}
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



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_show_all_datastores(one: One, datastores: List[Datastore]):
    datastore_ids       = [datastore.info().ID for datastore in datastores]
    datastorepool       = one.datastorepool.info().DATASTORE
    datastorepool_ids   = [datastore.ID for datastore in datastorepool]
    
    assert set(datastore_ids).issubset(datastorepool_ids)

