from utils      import run_command
from config     import COMMAND_EXECUTOR



def get_brestadm_auth() -> str:
    return run_command(COMMAND_EXECUTOR + " " + "cat /var/lib/one/homes/brestadm/one_auth")


