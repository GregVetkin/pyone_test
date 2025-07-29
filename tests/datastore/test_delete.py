import pytest
import pyone
from api                            import One
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import not_exist__test







def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)



def test_empty_datastore(one: One, dummy_datastore):
    delete__test(one.datastore, dummy_datastore)



def test_not_empty_datastore(one: One, dummy_image):
    datastore_id = one.image.info(dummy_image, False).DATASTORE_ID
    with pytest.raises(pyone.OneActionException):
        delete__test(one.datastore, datastore_id)


