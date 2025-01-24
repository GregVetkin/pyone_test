import pyone
import time

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"35b72dfa951b2b7e210cf2a84f55bf12d7e37a1c290e3d34f12c07b35cbcdac0"

API_URI = "http://raft.brest.local:2633/RPC2"


one = One(pyone.OneServer(API_URI, brestadm_auth))






one.vm.action("resume", 0)
