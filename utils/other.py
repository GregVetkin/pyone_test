import subprocess
import os
from time       import time_ns


def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"{e.stderr}")
        raise



def create_temp_file(size_mb: int, file_path: str):
    run_command(f"sudo dd if=/dev/urandom of={file_path} bs=1MiB count={size_mb} status=none")


def delete_temp_file(file_path: str):
    run_command(f"sudo rm -f {file_path}")


def get_unic_name(prefix: str = "api_test_", postfix: str = ""):
    return f"{prefix}{time_ns()}{postfix}"


def kinit(user: str, password: str, host: str = "$HOSTNAME"):
    kinit_command = f"echo '{password}' | kinit"
    ssh_command   = f"sshpass -p '{password}' ssh {user}@{host} \"{kinit_command}\""
    run_command(ssh_command)

