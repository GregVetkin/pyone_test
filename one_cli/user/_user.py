from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info, _update, _exist


FUNCTION_NAME = "oneuser"


def create_user(name: str, password: str = "12345678", driver: str = "public"):
    return int(run_command(f"sudo {FUNCTION_NAME} create {name} {password} --driver {driver} " + " | awk '{print $2}'"))


def user_exist(user_id: int) -> bool:
    return _exist(FUNCTION_NAME, user_id)


def get_user_id_by_name(user_name: str) -> int:
    return int(run_command(f"sudo {FUNCTION_NAME} list " + " | awk '{print $1 \" \" $2}' " + f" | grep {user_name} " + " | awk '{print $1}'"))



class User:
    def __init__(self, user_id: int) -> None:
        self._id        = user_id
        self._function  = FUNCTION_NAME

    def delete(self) -> None:
        _delete(self._function, self._id)

