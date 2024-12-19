from utils                  import run_command
from time                   import sleep   
from one_cli._base_commands import _info, _exist, _create, _info, _lock, _unlock
from one_cli.vm._common     import VirtualMachineInfo, parse_vm_info_from_xml


FUNCTION_NAME = "onevm"



def vm_exist(vm_id: int) -> bool:
    return _exist(FUNCTION_NAME, vm_id)


def create_vm(vm_template: str, await_vm_offline: bool = True) -> int:
    vm_id = _create(FUNCTION_NAME, vm_template)

    if await_vm_offline:
        wait_vm_offline(vm_id)

    return vm_id



def wait_vm_offline(vm_id: int, check_interval: float = 1.0) -> None:
    while True:
        if get_vm_state(vm_id) == "POWEROFF":
            break
        else:
            sleep(check_interval)


def get_vm_state(vm_id: int) -> str:
    return run_command(f"sudo {FUNCTION_NAME} show {vm_id} | grep STATE | head -n 1 " + " | awk '{print $3}'")





class VirtualMachine:
    def __init__(self, vm_id: int) -> None:
        self._id            = vm_id
        self._function      = FUNCTION_NAME
    

    def terminate(self, hard: bool = True) -> None:
        hard_flag = '--hard' if hard else ''
        run_command(f"sudo {self._function} terminate {self._id} {hard_flag}")


    def create_disk_snapshot(self, disk_id: int, snapshot_name: str) -> None:
        run_command(f"sudo {self._function} disk-snapshot-create {self._id} {disk_id} {snapshot_name}")


    def backup(self, datastore_id: int = -1, backup_name: str = "") -> None:
        backup_name     = f"-n {backup_name}" if backup_name else ""
        datastore_id    = f"-d {datastore_id}" if datastore_id != -1 else ""
        run_command(f"sudo {self._function} backup {self._id} {datastore_id} {backup_name}")


    def info(self) -> VirtualMachineInfo:
        return parse_vm_info_from_xml(_info(self._function, self._id, xml=True))


    def lock(self, lock_level: int = 1) -> None:
        _lock(self._function, self._id, lock_level)


    def unlock(self) -> None:
        _unlock(self._function, self._id)


    def disk_attach(self, image_id: int):
        run_command(f"sudo {self._function} disk-attach {self._id} -i {image_id}")


    def disk_detach(self, disk_id: int) -> None:
        run_command(f"sudo {self._function} disk-detach {self._id} {disk_id}")


    