import sys

from pyone      import OneServer
from api        import One

sys.path.append("api")



URL     = "http://bufn1.brest.local:2633/RPC2"
USER    = "brestadm"
TOKEN   = "ca62add7b4897b9e4e8a527ce2dfc63eafe83fd7a4401102bf13be0423c7ffe2"




one  = One(OneServer(URL, f"{USER}:{TOKEN}"))


vers = one.system.version()
conf = one.system.config()

