import os
from utils  import run_command
from time   import sleep




def create_vm_by_tempalte(image_template: str, await_vm_offline: bool = True) -> int:
    template_file_path  = "/tmp/test_template_file"

    with open(template_file_path, "w") as template_file:
        template_file.write(image_template)
    
    command     = f"sudo onevm create {template_file_path}" + " | awk '{print $2}'"
    vm_id       = int(run_command(command))

    if await_vm_offline:
        wait_vm_offline(vm_id)
        
    os.remove(template_file_path)
    return vm_id


def wait_vm_offline(vm_id: int, check_interval: float = 1.0) -> None:
    while True:
        if get_vm_state(vm_id) == "POWEROFF":
            break
        else:
            sleep(check_interval)


def get_vm_state(vm_id: int) -> str:
    command = f"sudo onevm show {vm_id} | grep STATE | head -n 1 " + " | awk '{print $3}'"
    return run_command(command)


def delete_vm(vm_id: int, hard: bool = True) -> None:
    command = f"sudo onevm delete {vm_id} "
    if hard:
        command += " --hard"
    run_command(command)
