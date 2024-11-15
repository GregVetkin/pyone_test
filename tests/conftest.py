import pytest

from pyone      import OneServer
from api        import One
from config     import API_URI
from utils      import get_user_auth





@pytest.fixture
def one(request):
    username  = request.param
    server    = OneServer(API_URI, get_user_auth(username))
    one       = One(server)
    
    yield one

    one._one_api.server_close()




