from utils  import run_command
from config import COMMAND_EXECUTOR


def get_user_id_by_name(user_name: str) -> int:
    command = COMMAND_EXECUTOR + " " + "oneuser list | awk '{print $1 \" \" $2}' " + f" | grep {user_name} " + " | awk '{print $1}'"
    return int(run_command(command))
