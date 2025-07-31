from api   import One

from tests._common_methods.info     import info__test, not_exist__test






def test_vm_not_exist(one: One):
    not_exist__test(one.vm)




def test_vm_info(one: One, dummy_vm: int):
    vm_id = dummy_vm
    info__test(one.vm, vm_id)


