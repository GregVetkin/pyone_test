from utils                  import run_command
from one_cli._base_commands import _delete, _info_dataclass, _update, _exist
from dataclasses            import dataclass



FUNCTION_NAME = "onegroup"



def create_group(name: str):
    return int(run_command(f"sudo {FUNCTION_NAME} create {name}" + " | awk '{print $2}'"))


def group_exist(group_id: int) -> bool:
    return _exist(FUNCTION_NAME, group_id)




class Group:
    def __init__(self, group_id: int) -> None:
        self._id        = group_id
        self._function  = FUNCTION_NAME

    def delete(self) -> None:
        _delete(self._function, self._id)

    def info(self) -> dataclass:
        return _info_dataclass(self._function, self._id)

    def addadmin(self, user_id: int) -> None:
        run_command(f"sudo {self._function} addadmin {self._id} {user_id}")

    def deladmin(self, user_id: int) -> None:
        run_command(f"sudo {self._function} deladmin {self._id} {user_id}")
    
    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)