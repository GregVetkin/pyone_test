import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"fa20ef55f090e3e00980a25b2f3876725b4aa6c6d32239410c802e5912487715"


# one = pyone.OneServer(API_URI, brestadm_auth)
# print(one.vm.disksaveas(10, 0, "saved_disk", "OS", -1))

API_URI = "http://bufn1.brest.local:2633/RPC2"
one = One(pyone.OneServer(API_URI, brestadm_auth))




print(one.vm.disksnapshotdelete(68, 1, 1))