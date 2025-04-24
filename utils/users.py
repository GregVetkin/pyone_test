from utils      import run_command
from config     import ALSE_VERSION



def get_user_auth(username: str) -> str:
    if ALSE_VERSION == 1.8:
        username += "@brest.local"
    return run_command(f"sudo cat /var/lib/one/homes/{username}/one_auth")


