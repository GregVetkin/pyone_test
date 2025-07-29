from api                            import One
from tests._common_methods.info     import info__test
from tests._common_methods.info     import not_exist__test




def test_datastore_not_exist(one: One):
    not_exist__test(one.datastore)


def test_datastore_info(one: One, dummy_datastore):
    info__test(one.datastore, dummy_datastore)

