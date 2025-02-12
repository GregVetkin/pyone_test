import pyone
import time

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"fa20ef55f090e3e00980a25b2f3876725b4aa6c6d32239410c802e5912487715"

API_URI = "http://bufn1.brest.local:2633/RPC2"


one = One(pyone.OneServer(API_URI, brestadm_auth))


vm_id = 0

snapshot_ids = [int(_id["SNAPSHOT_ID"]) for _id in one.vm.info(vm_id).TEMPLATE.get("SNAPSHOT", [])]
print(snapshot_ids)









