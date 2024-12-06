import pytest

from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME




@pytest.fixture(scope="module")
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



@pytest.fixture
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()



@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One, image: Image):
    with pytest.raises(OneException):
        one.vm.attach(999999, f"DISK=[IMAGE_ID={image._id}]")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_image_not_exist(one: One, vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.attach(vm._id, "DISK=[IMAGE_ID=999999]")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_attach_disk_to_vm(one: One, vm: VirtualMachine, image: Image):
    _id = one.vm.attach(vm._id, f"DISK=[IMAGE_ID={image._id}]")
    assert _id == vm._id
    
    from utils import run_command
    from one_cli._common import create_dataclass_from_xml
    from one_cli.vm         import wait_vm_offline
    import xml.etree.ElementTree as et
    wait_vm_offline(vm._id)
    vm_info = create_dataclass_from_xml(et.fromstring(run_command(f"sudo onevm show {vm._id} -x")))
    assert int(vm_info.TEMPLATE.DISK.IMAGE_ID) == image._id
