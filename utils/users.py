from utils      import run_command
from config     import COMMAND_EXECUTOR



def get_user_auth(username: str) -> str:
    return run_command(COMMAND_EXECUTOR + " " + f"cat /var/lib/one/homes/{username}/one_auth")


