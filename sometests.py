import pyone
from api import One



auth_url    = "http://bufn1.brest.local:2633/RPC2"
auth_user   = "brestadm"
auth_token  = "112cabb0345d2a47e1c9ab2f667c4e66f559d289180aa7974eab9f28a90cb06d"


client = pyone.OneServer(auth_url, session=auth_user + ':' + auth_token)



result = client.imagepool.info(-2, 259, 575).IMAGE



for _ in result:
    print(_.ID)


