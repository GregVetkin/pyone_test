import pytest
import pyone
from api                            import One
from tests._common_methods.chmod    import random_permissions__test





def test_datastore_not_exist(one: One):
    with pytest.raises(pyone.OneNoExistsException):
        one.datastore.chmod(99999)


def test_change_datastore_permissions(one: One, dummy_datastore):
    random_permissions__test(one.datastore, dummy_datastore)

