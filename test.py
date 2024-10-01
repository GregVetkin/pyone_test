import sys

from pyone      import OneServer
from api        import One
from utils      import create_user, delete_user, create_user_token

sys.path.append("api")
sys.path.append("utils")



URL     = "http://bufn1.brest.local:2633/RPC2"

user = "tester_admin"
create_user(user, "12345678", "brestadmins")

session = create_user_token(user, "brestadmins")
print(session)

one = One(OneServer(URL, session))

vers = one.system.version()
conf = one.system.config()

delete_user(user)

print(vers)
print(conf)