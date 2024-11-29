from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info, _update, _exist
from one_cli.group._common  import GroupInfo, parse_group_info_from_xml



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

    def info(self) -> GroupInfo:
        return parse_group_info_from_xml(_info(self._function, self._id, xml=True))

