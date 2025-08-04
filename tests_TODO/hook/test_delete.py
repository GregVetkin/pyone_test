from config.opennebula              import VmStates
from utils.other                    import wait_until
from api                            import One
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test








def test_hook_not_exist(one: One):
   delete_if_not_exist__test(one.hook)
   


def test_delete_empty_hoook(one: One, dummy_hook):
    delete__test(one.hook, dummy_hook)

