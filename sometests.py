import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"112cabb0345d2a47e1c9ab2f667c4e66f559d289180aa7974eab9f28a90cb06d"
one  = One(pyone.OneServer(API_URI, brestadm_auth))





res = one.zone.raftstatus()


print(res.has__content())