import pytest

from api            import One
from utils          import get_unic_name
from one_cli.host   import Host, create_host, host_exist
from one_cli.vm     import VirtualMachine, create_vm
from config         import ADMIN_NAME

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import cant_be_deleted__test




@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(f"{get_unic_name()}")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()


@pytest.fixture
def vm():
    _id = create_vm(f"NAME={get_unic_name()}\nCPU=1\nVCPU=1\nMEMORY=32")
    vm  = VirtualMachine(_id)
    yield vm
    vm.terminate()


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One):
   delete_if_not_exist__test(one.host)
   

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_host(one: One, host: Host):
    delete__test(one.host, host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_delete_host_with_vm(one: One, vm: VirtualMachine):
    i = 0
    while True:
        if host_exist(i) and (vm._id in Host(i).info().VMS):
            break
        i += 1

    cant_be_deleted__test(one.host, Host(i))
