import pytest

from pyone      import OneServer
from api        import One
from config     import API_URI






@pytest.fixture
def one(request):
    user_auth = request.param
    server    = OneServer(API_URI, user_auth)
    one       = One(server)
    
    yield one

    #one._one_api.server_close()




