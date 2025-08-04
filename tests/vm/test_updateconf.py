import pytest
import pyone
import random
import time

from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmLcmStates, VmStates
from config.base        import API_URI, BrestAdmin







# =================================================================================================
# TESTS
# ================================================================================================= 





def test_vm_not_exist(one: One):
    vm_id    = random.randint(9999, 999999)
    template = ""

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.updateconf(vm_id, template)





def test_updateconf_vm(one: One, dummy_vm: int):
    vm_id = dummy_vm

    attribute = "OS"
    sub_attribute = "ARCH"
    sub_attribute_value = "x86-64"
    template = f"""
        {attribute} = [
                    {sub_attribute}={sub_attribute_value}
                    ]
                """

    _id = one.vm.updateconf(vm_id, template)
    
    updated_template = one.vm.info(vm_id, True).TEMPLATE
    assert _id == vm_id
    assert attribute in updated_template
    assert sub_attribute in updated_template[attribute]
    assert sub_attribute_value == updated_template[attribute][sub_attribute]



@pytest.mark.KERBEROS
def test_updateconf_vm_KERBEROS(dummy_vm: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = dummy_vm

    attribute = "OS"
    sub_attribute = "ARCH"
    sub_attribute_value = "x86-64"
    template = f"""
        {attribute} = [
                    {sub_attribute}={sub_attribute_value}
                    ]
                """

    _id = one.vm.updateconf(vm_id, template, pw.sessionDir)
    pw.run_one_vm_action()
    
    updated_template = one.vm.info(vm_id, True).TEMPLATE
    assert _id == vm_id
    assert attribute in updated_template
    assert sub_attribute in updated_template[attribute]
    assert sub_attribute_value == updated_template[attribute][sub_attribute]
