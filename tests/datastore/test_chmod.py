from api                            import One
from tests._common_methods.chmod    import random_chmod__test, not_exist__test





def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


def test_random_chmod(one: One, dummy_datastore):
    random_chmod__test(one.datastore, dummy_datastore)

