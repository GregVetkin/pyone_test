import pytest
import time
import random

from api            import One
from pyone          import OneNoExistsException

from utils.version      import Version
from utils.other        import get_unic_name, wait_until
from utils.users        import get_api_connection_by_user_id
from utils.commands     import run_command_via_ssh
from utils.connection   import brest_admin_ssh_conn, local_admin_ssh_conn, BrestAdmin

from config.base        import BREST_VERSION
from config.opennebula  import VmStates, VmLcmStates, VmRecoverOperations



def __graceful_delete(one_method, one_object_id: int):
    try:
        one_method.delete(one_object_id)
    except OneNoExistsException:
        pass



@pytest.fixture
def one():
    user_id     = 2
    conn_data   = get_api_connection_by_user_id(user_id)
    one_api     = One(conn_data)

    yield one_api
    one_api._server.server_close()



@pytest.fixture
def dummy_datastore(one: One):
    """Creates empty image datastore, returns its id"""

    cluster_id = - 1
    template = f"""
        NAME    = {get_unic_name()}
        DS_MAD  = dummy
        TM_MAD  = dummy
        TYPE    = IMAGE_DS
    """
    datastore_id = one.datastore.allocate(template, cluster_id)

    yield datastore_id

    __graceful_delete(one.datastore, datastore_id)




@pytest.fixture
def dummy_image(one: One, dummy_datastore):
    """Creates datablock image in dummy_datastore, returns its id"""

    template = f"""
        NAME = {get_unic_name()}
        SIZE = 1
        TYPE = DATABLOCK
    """
    datastore_id = dummy_datastore
    check_storage_capacity = False
    image_id = one.image.allocate(template, datastore_id, check_storage_capacity)

    yield image_id

    __graceful_delete(one.image, image_id)



@pytest.fixture
def dummy_vm(one: One):
    """Creates vm without disks, returns its id"""

    template = f"""
        NAME = {get_unic_name()}
        CPU  = 0.01
        MEMORY = 1
    """
    hold_vm = False
    vm_id = one.vm.allocate(template, hold_vm)

    yield vm_id

    if one.vm.info(vm_id, False).STATE != VmStates.DONE:
        one.vm.recover(vm_id, VmRecoverOperations.DELETE)



@pytest.fixture
def dummy_group(one: One):
    """Creates group without users, returns its id"""

    group_name = get_unic_name()
    group_id = one.group.allocate(group_name)

    yield group_id

    __graceful_delete(one.group, group_id)



@pytest.fixture
def dummy_user(one: One):
    """Creates user with group by default (brestusers), returns its id"""

    user_name = get_unic_name()
    user_password = "12345678"
    auth_driver = ""
    group_ids = []
    user_id = one.user.allocate(user_name, user_password, auth_driver, group_ids)

    yield user_id

    __graceful_delete(one.user, user_id)



@pytest.fixture
def dummy_cluster(one: One):
    """Creates cluster (empty), returns its id"""

    cluster_name = get_unic_name()
    cluster_id = one.cluster.allocate(cluster_name)

    yield cluster_id

    __graceful_delete(one.cluster, cluster_id)



@pytest.fixture
def dummy_host(one: One):
    """Creates host (unreachable), returns its id"""

    host_name = get_unic_name()
    im_mad = "kvm"
    vm_mad = "kvm"
    cluster_id = -1
    host_id = one.host.allocate(host_name, im_mad, vm_mad, cluster_id)

    yield host_id

    __graceful_delete(one.host, host_id)



@pytest.fixture
def dummy_template(one: One):
    """Creates empty template, returns its id"""

    template = f"""
        NAME = {get_unic_name()}
    """
    template_id = one.template.allocate(template)

    yield template_id

    __graceful_delete(one.template, template_id)



@pytest.fixture
def dummy_vnet(one: One):
    """Creates empty virtual network (withouth addr), returns its id"""

    template = f"""
        NAME   = {get_unic_name()}
        VN_MAD = bridge
    """
    cluster_id = -1
    vnet_id = one.vn.allocate(template, cluster_id)

    yield vnet_id

    __graceful_delete(one.vn, vnet_id)




@pytest.fixture
def poweroff_vm_mini(one: One):
    if Version(BREST_VERSION) < Version("4"):
        script_dir = "~/brest"
        ssh_conn   = local_admin_ssh_conn
    else:
        script_dir = "/opt/brest"
        ssh_conn   = brest_admin_ssh_conn
    
    vm_name = f"api_test_{random.randint(0, 9999)}" # С длинным именем из get_unic_name(), cli_prepare.sh не отрабатывает отлов статуса ВМ
    command = f"cd {script_dir} && ./cli_prepare.sh create_vm mini {vm_name} nonpers"
    
    run_command_via_ssh(ssh_conn, command)
    vm_id = next(vm.ID for vm in one.vmpool.info(-2, -1, -1, -2, "").VM if vm.NAME == vm_name)

    yield vm_id

    if one.vm.info(vm_id, False).STATE != VmStates.DONE:
        run_command_via_ssh(brest_admin_ssh_conn, f"onevm terminate {vm_id} --hard")


@pytest.fixture
def running_vm_mini(one: One, poweroff_vm: int):
    vm_id = poweroff_vm
    run_command_via_ssh(brest_admin_ssh_conn, f"echo '{BrestAdmin.PASSWORD}' | kinit; onevm resume {vm_id}")
    wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.RUNNING)
    yield vm_id