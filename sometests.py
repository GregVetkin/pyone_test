import pyone

from api            import One
from config         import BRESTADM, API_URI
from utils.users    import get_user_auth

one  = One(pyone.OneServer(API_URI, get_user_auth(BRESTADM)))



templ = """
    NAME = test2222
"""
# result = one.template.instantiate(80, "testing", extra_template="MEMORY=32\nCPU=0.1")
# print(result)

one.image.lock(1213, 4)