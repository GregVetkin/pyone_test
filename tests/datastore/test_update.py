import pytest

from api                            import One
from tests._common_methods.update   import update__test, not_exist__test







def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_datastore: int, update_type: int):
    datastore_id = dummy_datastore
    update__test(one.datastore, datastore_id, update_type)


