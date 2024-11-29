import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"145958aaa8d89a5c9ba6eed3a146fda9a4634425b8c3942b913faf6e4ff085d2"


one  = One(pyone.OneServer(API_URI, brestadm_auth))





res = one.group.deladmin(100, 2)
print(res)



# from one_cli.group import Group
# print(Group(115).info().IMAGE_QUOTA)
# print(Group(115).info().TEMPLATE)
# print(Group(0).info().IMAGE_QUOTA)



# import xmlrpc.client

# server = xmlrpc.client.ServerProxy(API_URI)


# session_string = brestadm_auth
# user_name = "keker"
# token = ""
# period = -1
# gid = 2


# response = server.one.groupquota.info(session_string)

# print(response)

