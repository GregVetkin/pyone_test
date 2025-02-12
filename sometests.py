import pyone
import time

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"fa20ef55f090e3e00980a25b2f3876725b4aa6c6d32239410c802e5912487715"

API_URI = "http://bufn1.brest.local:2633/RPC2"


one = One(pyone.OneServer(API_URI, brestadm_auth))



records = one.vmpool.monitoring().MONITORING
print(len(records))


counter = 0

while True:
    records = one.vmpool.monitoring().MONITORING
    time.sleep(1)
    counter += 1
    print("Second ", counter, " | ", "Records: ", len(records))

