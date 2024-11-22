import pyone

from api            import One
from config         import ADMIN_NAME, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(ADMIN_NAME)))

zone_template = """

    NAME = test
    ENDPOINT = test


"""





from utils import federation_master, federation_standalone
from utils.opennebula import _get_federation_mode


# print(_get_federation_mode())
# federation_standalone()
# print(_get_federation_mode())

# from utils import run_command
# from config import COMMAND_EXECUTOR


# print(one.zone.allocate(zone_template))
print(_get_federation_mode())
