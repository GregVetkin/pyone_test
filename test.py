import sys

from pyone      import OneServer
from api        import One
from utils      import create_user, delete_user, create_user_token

sys.path.append("api")
sys.path.append("utils")



URL     = "http://bufn1.brest.local:2633/RPC2"



one = One(OneServer(URL, "brestadm:ca62add7b4897b9e4e8a527ce2dfc63eafe83fd7a4401102bf13be0423c7ffe2"))

vers = one.system.version()
conf = one.system.config()


print(vers)
print(conf)