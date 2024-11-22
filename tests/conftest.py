import pytest

from pyone              import OneServer
from api                import One
from config             import API_URI, COMMAND_EXECUTOR, RAFT_CONFIG
from utils              import get_user_auth, restart_opennebula, run_command
from utils.opennebula   import _get_federation_mode, _change_federation_mode





@pytest.fixture
def one(request):
    username  = request.param
    server    = OneServer(API_URI, get_user_auth(username))
    one       = One(server)
    
    yield one

    one._one_api.server_close()





@pytest.fixture
def federation_mode(request):
    changed     = False
    mode        = request.param
    copy_path   = "/tmp/raft_orig.conf"

    if _get_federation_mode() != mode:
        run_command(COMMAND_EXECUTOR + " " + f"cp -p {RAFT_CONFIG} {copy_path}")
        _change_federation_mode(mode)
        changed = True

    yield

    if changed:
        run_command(COMMAND_EXECUTOR + " " + f"cat {copy_path} > sudo tee {RAFT_CONFIG}")
        run_command(COMMAND_EXECUTOR + " " + f"rm -f {copy_path}")
        restart_opennebula()

