from api import One
from pyone import OneServer


URL     = "http://bufn1.brest.local:2633/RPC2"
one     = OneServer(URL, "brestadm:ca62add7b4897b9e4e8a527ce2dfc63eafe83fd7a4401102bf13be0423c7ffe2")
config = one.system.config()

print(config.has__content())