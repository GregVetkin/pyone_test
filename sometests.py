import pyone
import time

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"92e18650e8b0f8cd173e01115798937e9c632315693982f526b8be10adee29bc"

API_URI = "http://bufn1.brest.local:2633/RPC2"


one = One(pyone.OneServer(API_URI, brestadm_auth))




print(type(one.vm.info(0).HISTORY_RECORDS.HISTORY[-1].DS_ID))