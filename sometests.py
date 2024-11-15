import pyone

from api            import One
from config         import BRESTADM, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(BRESTADM)))



templ = """
        NAME    = Hash #44
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
"""
# result = one.template.instantiate(80, "testing", extra_template="MEMORY=32\nCPU=0.1")
# print(result)

# template_xml = "<VMTEMPLATE><NAME>TEST</NAME></VMTEMPLATE>"
# one.template.allocate(template_xml)

from one_cli.host import Host, host_exist
from one_cli.vm   import VirtualMachine, create_vm



templ = """
NAME = ssss
CPU = 1
VCPU = 1
MEMORY = 32
"""
vm_id = create_vm(templ, True)
print(f"vm is ready with id {vm_id}")


i = 0
while True:
        if host_exist(i) and (vm_id in Host(i).info().VMS):
                break
        i += 1
    

print(f"vm on host with id {i}")