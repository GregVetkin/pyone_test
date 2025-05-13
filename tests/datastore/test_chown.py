from api                            import One
from tests._common_methods.chown    import object_not_exist__test
from tests._common_methods.chown    import user_not_exist__test
from tests._common_methods.chown    import group_not_exist__test
from tests._common_methods.chown    import user_and_group_change__test
from tests._common_methods.chown    import user_and_group_not_changed__test
from tests._common_methods.chown    import user_change__test
from tests._common_methods.chown    import group_change__test








def test_datastore_not_exist(one: One):
    object_not_exist__test(one.datastore)




def test_user_not_exist(one: One, dummy_datastore):
    user_not_exist__test(one.datastore, dummy_datastore)




def test_group_not_exist(one: One, dummy_datastore):
    group_not_exist__test(one.datastore, dummy_datastore)




def test_user_and_group_change(one: One, dummy_datastore, dummy_user, dummy_group):
    user_and_group_change__test(one.datastore, dummy_datastore, dummy_user, dummy_group)




def test_user_and_group_not_changed(one: One, dummy_datastore):
    user_and_group_not_changed__test(one.datastore, dummy_datastore)




def test_only_user_change(one: One, dummy_datastore, dummy_user):
    user_change__test(one.datastore, dummy_datastore, dummy_user)




def test_only_group_change(one: One, dummy_datastore, dummy_group):
    group_change__test(one.datastore, dummy_datastore, dummy_group)
