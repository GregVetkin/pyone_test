import pyone
from api import One

auth_url = "http://bufn1.brest.local:2633/RPC2"
auth_user = "brestadm"
auth_token="c709ad80eab3785053665faa66c6a141c57cc2b13d3d37c710ecbc9d2df660c4"

client = pyone.OneServer(auth_url, session=auth_user + ':' + auth_token)






result = One(client).image.clone(1, "ggga", 2)
print(result)
