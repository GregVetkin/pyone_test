from api                            import One
from tests._common_methods.update   import update_and_merge__test
from tests._common_methods.update   import update_and_replace__test
from tests._common_methods.update   import update_if_not_exist__test






def test_not_exist(one: One):
    update_if_not_exist__test(one.datastore)


def test_update_by_replace(one: One, dummy_datastore):
    datastore_id = dummy_datastore
    update_and_replace__test(one.datastore, datastore_id)


def test_update_by_merge(one: One, dummy_datastore):
    datastore_id = dummy_datastore
    update_and_merge__test(one.datastore, datastore_id)

