import pyone
from api import One



auth_url    = "http://bufn1.brest.local:2633/RPC2"
auth_user   = "brestadm"
auth_token  = "145958aaa8d89a5c9ba6eed3a146fda9a4634425b8c3942b913faf6e4ff085d2"


client = pyone.OneServer(auth_url, session=auth_user + ':' + auth_token)




result = One(client).host.info(0)




print(result.get_STATE())