import pyone
from api import One



auth_url    = "http://bufn1.brest.local:2633/RPC2"
auth_user   = "brestadm"
auth_token  = "145958aaa8d89a5c9ba6eed3a146fda9a4634425b8c3942b913faf6e4ff085d2"


server  = pyone.OneServer(auth_url, session=auth_user + ':' + auth_token)
one     = One(server)


# templ = """
#     NAME    = test2222
#     CPU     = 1
#     VCPU    = 2
#     MEMORY  = 4096
#     DISK    = [IMAGE_ID = 1195]
# """



# result = one.template.chmod(4, 1, 1, 1, 1, 1, 1, 1, 1, 1, True)


# print(result)

assert {54, 55, 56} == set([54, 55, 56])