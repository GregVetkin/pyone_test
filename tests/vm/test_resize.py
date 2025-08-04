import pytest
import pyone
import random
import time


from api                import One
from utils.kerberos     import PyoneWrap
from config.base        import API_URI, BrestAdmin


    




# =================================================================================================
# TESTS
# =================================================================================================


def test_vm_not_exist(one: One):
    vm_id       = random.randint(9999, 999999)
    tempalte    = ""
    check_host  = True

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.resize(vm_id, tempalte, check_host)



@pytest.mark.KERBEROS
def test_vm_resize_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id = poweroff_vm_mini

    new_cpu    = round(random.uniform(0.1, 3.9), 2)
    new_vcpu   = random.randint(1, 3)
    new_memory = random.randint(1, 3072)

    check_host = True
    template = f"""
        CPU    = {new_cpu}
        VCPU   = {new_vcpu}
        MEMORY = {new_memory}
    """
    

    _id = one.vm.resize(vm_id, template, check_host, pw.sessionDir)
    pw.run_one_vm_action()

    template_after = one.vm.info(vm_id, False).TEMPLATE
    cpu_after      = float(template_after["CPU"])
    vcpu_after     = int(template_after["VCPU"])
    memory_after   = int(template_after["MEMORY"])

    assert _id == vm_id
    assert cpu_after == new_cpu
    assert vcpu_after == new_vcpu
    assert memory_after == new_memory




@pytest.mark.parametrize("check_host", [True, False])
def test_check_host_capacity(one: One, poweroff_vm_mini: int, check_host: bool):
    vm_id = poweroff_vm_mini

    template_before = one.vm.info(vm_id, False).TEMPLATE
    cpu_before      = float(template_before["CPU"])
    vcpu_before     = int(template_before["VCPU"])
    memory_before   = int(template_before["MEMORY"])

    new_cpu     = 999
    new_memory  = 9999999999

    template = f"""
        CPU     = {new_cpu}
        MEMORY  = {new_memory}
    """



    if not check_host:
        _id = one.vm.resize(vm_id, template, check_host)
        assert _id == vm_id

        template_after = one.vm.info(vm_id, False).TEMPLATE
        cpu_after      = float(template_after["CPU"])
        vcpu_after     = int(template_after["VCPU"])
        memory_after   = int(template_after["MEMORY"])

        assert cpu_after == new_cpu
        assert vcpu_after == vcpu_before
        assert memory_after == new_memory

    else:
        with pytest.raises(pyone.OneActionException):
            one.vm.resize(vm_id, template, check_host)

        template_after = one.vm.info(vm_id, False).TEMPLATE
        cpu_after      = float(template_after["CPU"])
        vcpu_after     = int(template_after["VCPU"])
        memory_after   = int(template_after["MEMORY"])

        assert cpu_after == cpu_before
        assert vcpu_after == vcpu_before
        assert memory_after == memory_before
