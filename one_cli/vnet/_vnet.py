from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info, _update, _exist, _create


FUNCTION_NAME = "onevnet"


def vnet_exist(vnet_id: int) -> bool:
    return _exist(FUNCTION_NAME, vnet_id)


def create_vnet(vnet_template: str) -> int:
    return _create(FUNCTION_NAME, vnet_template)




class Vnet:
    def __init__(self, vnet_id: int) -> None:
        self._id        = vnet_id
        self._function  = FUNCTION_NAME

    def delete(self) -> None:
        _delete(self._function, self._id)

