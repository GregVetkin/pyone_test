import pytest

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME
from pyone              import OneException



@pytest.fixture()
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.updateconf(999999, template="")




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_updateconf_vm(one: One, vm: VirtualMachine):
    attribute = "OS"
    sub_attribute = "ARCH"
    sub_attribute_value = "x86-64"
    template = f"""
        {attribute} = [
                    {sub_attribute}={sub_attribute_value}
                    ]"""


    _id = one.vm.updateconf(vm._id, template)
    assert _id == vm._id
    updated_template = one.vm.info(vm._id).TEMPLATE
    assert attribute in updated_template
    assert sub_attribute in updated_template[attribute]
    assert sub_attribute_value == updated_template[attribute][sub_attribute]
