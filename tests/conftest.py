import pytest
from pyone              import OneNoExistsException
from utils.other        import get_unic_name
from utils.users        import get_api_connection_by_user_id
from api                import One



@pytest.fixture
def one(request):
    user_id     = request.param
    conn_data   = get_api_connection_by_user_id(user_id)
    one_api     = One(conn_data)

    yield one_api
    one_api._server.server_close()


@pytest.fixture
def dummy_datastore(one: One):
    """Creates empty image datastore, returns its id"""

    template = f"""
        NAME    = {get_unic_name()}
        DS_MAD  = dummy
        TM_MAD  = dummy
        TYPE    = IMAGE_DS
    """
    datastore_id = one.datastore.allocate(template, -1)
    yield datastore_id
    try:
        one.datastore.delete(datastore_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_image(one: One, dummy_datastore):
    """Creates datablock image in dummy_datastore, returns its id"""

    datastore_id = dummy_datastore
    template = f"""
        NAME = {get_unic_name()}
        SIZE = 1
        TYPE = DATABLOCK
    """
    image_id = one.image.allocate(template, datastore_id, False)
    yield image_id
    try:
        one.image.delete(image_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_vm(one: One):
    """Creates vm without disks, returns its id"""

    template = f"""
        NAME = {get_unic_name()}
        CPU  = 0.01
        MEMORY = 1
    """
    vm_id = one.vm.allocate(template, False)
    yield vm_id
    try:
        one.vm.action("terminate-hard", vm_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_group(one: One):
    """Creates group without users, returns its id"""

    group_id = one.group.allocate(get_unic_name())
    yield group_id
    try:
        one.group.delete(group_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_user(one: One):
    """Creates user with group by default (brestusers), returns its id"""

    user_id = one.user.allocate(get_unic_name(), password="12345678")
    yield user_id
    try:
        one.user.delete(user_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_cluster(one: One):
    """Creates cluster (empty), returns its id"""

    cluster_id = one.cluster.allocate(get_unic_name())
    yield cluster_id
    try:
        one.cluster.delete(cluster_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_host(one: One):
    """Creates host (unreachable), returns its id"""

    host_id = one.host.allocate(get_unic_name())
    yield host_id
    try:
        one.host.delete(host_id)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_template(one: One):
    """Creates empty template, returns its id"""

    template = f"""
        NAME = {get_unic_name()}
    """
    template_id = one.template.allocate(template)
    yield template_id
    try:
        one.template.delete(template_id, False)
    except OneNoExistsException:
        pass


@pytest.fixture
def dummy_vnet(one: One):
    """Creates empty virtual network (withouth addr), returns its id"""

    template = f"""
        NAME   = {get_unic_name()}
        VN_MAD = bridge
    """
    vnet_id = one.vn.allocate(template, -1)
    yield vnet_id
    try:
        one.vn.delete(vnet_id)
    except OneNoExistsException:
        pass
