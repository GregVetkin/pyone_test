import pyone
from api import One



auth_url    = "http://bufn1.brest.local:2633/RPC2"
auth_user   = "brestadm"
auth_token  = "145958aaa8d89a5c9ba6eed3a146fda9a4634425b8c3942b913faf6e4ff085d2"


client = pyone.OneServer(auth_url, session=auth_user + ':' + auth_token)




# result = One(client).datastore.update(321, "TM_MAD = dev", replace=True)

# print(result)

# from one_cli.datastore import Datastore

# ds = Datastore(321)
# templ = """
# TM_MAD = dummy
# d1 = HAHAHA
# """
# ds.update(templ, False)
res = client.zone.raftstatus()
print(res)