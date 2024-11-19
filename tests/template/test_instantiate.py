import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_unic_name
from one_cli.template   import Template, create_template, template_exist
from one_cli.vm         import VirtualMachine, create_vm, vm_exist
from config             import ADMIN_NAME





@pytest.fixture
def vmtemplate():
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    _id = create_template(template)
    the_template = Template(_id)
    yield the_template
    the_template.delete()
    



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.template.instantiate(999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_instantiane_vm(one: One, vmtemplate: Template):
    vm_id = one.template.instantiate(vmtemplate._id, vm_name=get_unic_name())
    vm    = VirtualMachine(vm_id)
    assert vm_exist(vm._id)
    vm.terminate()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_instantiane_and_hold_vm(one: One, vmtemplate: Template):
    vm_id = one.template.instantiate(vmtemplate._id, vm_name=get_unic_name(), hold_vm=True)
    vm    = VirtualMachine(vm_id)
    assert vm.info().STATE == 2
    vm.terminate()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_instantiane_vm_with_extra_tempalte(one: One, vmtemplate: Template):
    extra_attribute = "TEST_ATTRIBUTE"
    vm_id = one.template.instantiate(vmtemplate._id, vm_name=get_unic_name(), extra_template=f"{extra_attribute} = TEST")
    vm    = VirtualMachine(vm_id)
    assert extra_attribute in vm.info().USER_TEMPALTE
    vm.terminate()


