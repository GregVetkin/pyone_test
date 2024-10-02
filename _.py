import pyone




URL     = "http://bufn1.brest.local:2633/RPC2"



#one = pyone.OneServer(URL, "test:9f232fe3e7c46821fa94d50f5d78a8b1f9bca2f44173c296ced3beb00a3456e6")
one = pyone.OneServer(URL, "brestadm:ca62add7b4897b9e4e8a527ce2dfc63eafe83fd7a4401102bf13be0423c7ffe2")
print(type(one.system.config()))