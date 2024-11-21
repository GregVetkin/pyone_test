import pyone

from api            import One
from config         import ADMIN_NAME, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(ADMIN_NAME)))


from one_cli.vm import VirtualMachine

# one.template.instantiate(26, private_persistent_copy=True)


one.host.lock(30, 4)