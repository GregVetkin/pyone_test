import pytest
import random
from api            import One
from utils.other    import get_unic_name



@pytest.fixture
def datastore_ids(one: One):
    datastore_ids_list = []
    for _ in range(random.randint(3, 10)):
        datastore_id = one.datastore.allocate(f"NAME={get_unic_name()}\nDS_MAD=dummy\nTM_MAD=dummy\nTYPE=IMAGE_DS")
        datastore_ids_list.append(datastore_id)
    yield datastore_ids_list
    for ds_id in datastore_ids_list:
        one.datastore.delete(ds_id)






def test_get_all_datastores_info(one: One, datastore_ids):
    datastorepool_ids = [datastore.ID for datastore in one.datastorepool.info().DATASTORE]
    assert set(datastore_ids).issubset(datastorepool_ids)

