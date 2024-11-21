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




# from utils.other import get_federation_mode, change_federation_mode

# print(get_federation_mode())
# change_federation_mode("MASTER")
# print(get_federation_mode())


from one_cli.zone import Zone, create_zone


_id = create_zone("NAME=test3\nENDPOINT=http://localhost:2633/RPC2")
print(_id)
