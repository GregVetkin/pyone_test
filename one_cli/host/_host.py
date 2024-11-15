from config                 import COMMAND_EXECUTOR
from utils                  import run_command
from one_cli._base_commands import _delete, _info, _update, _exist, _rename, _enable, _disable, _offline
from one_cli.host._common   import HostInfo, parse_host_info_from_xml


FUNCTION_NAME = "onehost"


def create_host(name: str):
    return int(run_command(COMMAND_EXECUTOR + " " + f"{FUNCTION_NAME} create {name}" + " | awk '{print $2}'"))


def host_exist(host_id: int) -> bool:
    return _exist(FUNCTION_NAME, host_id)




class Host:
    def __init__(self, host_id: int) -> None:
        self._id        = host_id
        self._function  = FUNCTION_NAME


    def delete(self) -> None:
        _delete(self._function, self._id)


    def rename(self, new_name: str) -> None:
        _rename(self._function, self._id, new_name)


    def enable(self) -> None:
        _enable(self._function, self._id)


    def disable(self) -> None:
        _disable(self._function, self._id)


    def offline(self) -> None:
        _offline(self._function, self._id)


    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)


    def info(self) -> HostInfo:
        return parse_host_info_from_xml(_info(self._function, self._id, xml=True))