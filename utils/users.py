from utils      import run_command



def get_user_auth(username: str) -> str:
    return run_command(f"sudo cat /var/lib/one/homes/{username}/one_auth")


