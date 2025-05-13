from api                            import One
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test









def test_datastore_not_exist(one: One):
    delete_if_not_exist__test(one.datastore)



def test_delete_empty_datastore(one: One, dummy_datastore):
    delete__test(one.datastore, dummy_datastore)



def test_delete_not_empty_datastore(one: One, dummy_image):
    not_empty_dsatastore_id = one.image.info(dummy_image).DATASTORE_ID
    cant_be_deleted__test(one.datastore, not_empty_dsatastore_id)

