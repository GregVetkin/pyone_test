import subprocess
import re

from config import COMMAND_EXECUTOR
from time import time_ns


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
    run_command(COMMAND_EXECUTOR + " " + f"dd if=/dev/urandom of={file_path} bs=1MiB count={size_mb} status=none")


def delete_temp_file(file_path: str):
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {file_path}")


def get_unic_name(prefix: str = "api_test_", postfix: str = ""):
    return f"{prefix}{time_ns()}{postfix}"



def restart_opennebula():
    run_command(COMMAND_EXECUTOR + " " + "systemctl restart opennebula")



def get_federation_mode() -> str:
    content = run_command(COMMAND_EXECUTOR + " " + "cat /etc/one/one.d/raft.conf")
    
    federation_match = re.search(
        r'FEDERATION\s*=\s*\[\s*(.*?)\s*\]',
        content,
        re.DOTALL
    )

    if federation_match:
        federation_block = federation_match.group(1)
        mode_match = re.search(r'MODE\s*=\s*["\'](.+?)["\']', federation_block)

        if mode_match:
            return mode_match.group(1)
    
    return None



def change_federation_mode(mode: str) -> None:
    content = run_command(COMMAND_EXECUTOR + " " + "cat /etc/one/one.d/raft.conf")
    
    federation_match = re.search(
        r'FEDERATION\s*=\s*\[\s*(.*?)\s*\]',
        content,
        re.DOTALL
    )

    if federation_match:
        federation_block = federation_match.group(1)
        
        new_federation_block = re.sub(
            r'MODE\s*=\s*["\'](.+?)["\']',
            f'MODE = "{mode}"',
            federation_block
        )

        content = content.replace(
            federation_block,
            new_federation_block
        )

        if "ssh" in COMMAND_EXECUTOR:
            run_command(COMMAND_EXECUTOR + " " + f"\'tee /etc/one/one.d/raft.conf << EOF\n{content}\nEOF\'")
        else:
            run_command(COMMAND_EXECUTOR + " " + f"tee /etc/one/one.d/raft.conf << EOF\n{content}\nEOF")
        
        restart_opennebula()
