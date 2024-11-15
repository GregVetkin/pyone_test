import pyone

from api            import One
from config         import BRESTADM, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(BRESTADM)))



templ = """
        NAME    = templ_with_img
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
        DISK    = [IMAGE_ID = 1710]
        DISK    = [IMAGE_ID = 1721]
"""
# result = one.template.instantiate(80, "testing", extra_template="MEMORY=32\nCPU=0.1")
# print(result)

# one.template.allocate(templ)





