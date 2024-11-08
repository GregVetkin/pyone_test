from config                 import COMMAND_EXECUTOR
from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info, _update, _exist



def create_user(name: str, password: str = "12345678", driver: str = "public"):
    return int(run_command(COMMAND_EXECUTOR + " " + f"oneuser create {name} {password}, --driver {driver} " + " | awk '{print $2}'"))


def user_exist(user_id: int) -> bool:
    return _exist("oneuser", user_id)




class User:
    def __init__(self, user_id: int) -> None:
        self._id        = user_id
        self._function  = "oneuser"

    def delete(self) -> None:
        _delete(self._function, self._id)

