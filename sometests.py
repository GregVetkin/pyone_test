
import pyone
from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"0776469fdb010e361440f8eacde8a872ddf36a6b9f8053ff84016e2621a7c797"
# brestadm_auth = "tester:f93c22104ac19e027d6259153bc1cba6e98c93337d87ef695cc95ea6f18ad617"

API_URI = "http://raft.brest.local:2633/RPC2"


one = One(pyone.OneServer(API_URI, brestadm_auth))

templ = """
CPU=99999
"""

res = one.vm.resize(36, templ, False)
print(res)



# import pyone

# client = pyone.OneServer(API_URI, session=brestadm_auth)
# res = client.vm.attachsg()
# print(res)