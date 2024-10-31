from config         import COMMAND_EXECUTOR
from utils          import run_command
from time           import sleep   




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
        self._vm_id = vm_id
    
    def terminate(self, hard: bool = True) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onevm terminate {self._vm_id} {'--hard' if hard else ''}")