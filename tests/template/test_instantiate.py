import pytest
from time               import sleep
from api                import One
from pyone              import OneNoExistsException
from utils              import get_unic_name
from one_cli.template   import Template, create_template, template_exist
from one_cli.image      import Image, create_image, image_exist, wait_image_ready
from one_cli.datastore  import Datastore, create_datastore
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
    
    
@pytest.fixture(scope="module")
def datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(template)
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
    if not image_exist(image_id):
        return
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()
    

@pytest.fixture
def image_2(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    if not image_exist(image_id):
        return
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()


@pytest.fixture
def vmtemplate_with_images(image: Image, image_2: Image):
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
        DISK    = [IMAGE_ID = {image._id}]
        DISK    = [IMAGE_ID = {image_2._id}]
    """
    _id = create_template(template)
    the_template = Template(_id)

    yield the_template
    
    if not template_exist(_id):
        return
    
    if the_template.info().LOCK is not None:
        the_template.unlock()

    the_template.delete()


@pytest.fixture
def purge_vm_after_test():
    vm_id = None

    def _get_vm_id(_id):
        nonlocal vm_id
        vm_id = _id

    yield _get_vm_id

    if vm_id is not None:
        vm = VirtualMachine(vm_id)
        vm_info  = vm.info()
        vm_disks = [Image(_["IMAGE_ID"]) for _ in vm_info.TEMPLATE["DISK"]]
        template_id = int(vm_info.TEMPLATE["TEMPLATE_ID"])
        
        vm.terminate()
        Template(template_id).delete()

        for disk in vm_disks:
            wait_image_ready(disk._id)
            disk.delete()








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
    assert extra_attribute in vm.info().USER_TEMPLATE
    vm.terminate()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_create_as_persistent_vm(one: One, vmtemplate_with_images: Template, purge_vm_after_test):
    vm_id = one.template.instantiate(vmtemplate_with_images._id, private_persistent_copy=True)
    purge_vm_after_test(vm_id)
    sleep(5)
    vm = VirtualMachine(vm_id)
    vm_disks = [Image(_["IMAGE_ID"]) for _ in vm.info().TEMPLATE["DISK"]]
    
    assert vm_exist(vm_id)
    
    for disk in vm_disks:
        disk_info = disk.info()
        assert image_exist(disk._id)
        assert vm_id in disk_info.VMS
        assert disk_info.STATE == 8 # pers PERS_USED
        assert disk_info.PERSISTENT
        
    
    
    