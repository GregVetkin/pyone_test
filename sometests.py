import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"145958aaa8d89a5c9ba6eed3a146fda9a4634425b8c3942b913faf6e4ff085d2"
one  = One(pyone.OneServer(API_URI, brestadm_auth))




res = one.cluster.adddatastore(104, 1)
print(res)

