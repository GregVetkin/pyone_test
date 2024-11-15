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




