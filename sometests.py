import pyone

from api            import One
from config         import ADMIN_NAME, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(ADMIN_NAME)))

# zone_template = """

#     NAME = test
#     ENDPOINT = test


# """
# result = one.zone.detele()




from utils.other import get_federation_mode, change_federation_mode

print(get_federation_mode())
change_federation_mode("STANDALONE")
print(get_federation_mode())

# from utils import run_command
# from config import COMMAND_EXECUTOR


print(one.zone.raftstatus())

