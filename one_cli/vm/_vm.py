from config         import COMMAND_EXECUTOR
from utils          import run_command
from time           import sleep   



def vm_exist(vm_id: int) -> bool:
    exec_code = int(run_command(COMMAND_EXECUTOR + " " + f"onevm show {vm_id} &>/dev/null; echo $?"))
    return True if exec_code == 0 else False



def create_vm_by_tempalte(vm_template: str, await_vm_offline: bool = True) -> int:
    template_file_path  = "/tmp/test_template_file"

    if "ssh" in COMMAND_EXECUTOR:
        run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {template_file_path}\n{vm_template}\nEOF\'")
    else:
        run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {template_file_path}\n{vm_template}\nEOF")

    vm_id = int(run_command(COMMAND_EXECUTOR + " " + f"onevm create {template_file_path}" + " | awk '{print $2}'"))
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {template_file_path}")

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
    command = COMMAND_EXECUTOR + " " + f"onevm show {vm_id} | grep STATE | head -n 1 " + " | awk '{print $3}'"
    return run_command(command)





class VirtualMachine:
    def __init__(self, vm_id: int) -> None:
        self._id = vm_id
    
    def terminate(self, hard: bool = True) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onevm terminate {self._id} {'--hard' if hard else ''}")

    def create_disk_snapshot(self, disk_id: int, snapshot_name: str) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onevm disk-snapshot-create {self._id} {disk_id} {snapshot_name}")

    def backup(self, datastore_id: int = -1, backup_name: str = "") -> None:
        backup_name     = f"-n {backup_name}" if backup_name else ""
        datastore_id    = f"-d {datastore_id}" if datastore_id != -1 else ""
        run_command(COMMAND_EXECUTOR + " " + f"onevm backup {self._id} {datastore_id} {backup_name}")
    