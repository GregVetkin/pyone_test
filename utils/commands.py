import subprocess
import shlex

from utils.connection import SshConnectionData


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



def run_command_via_ssh(ssh_connection_data: SshConnectionData, command: str) -> str:
    username     = ssh_connection_data.user
    password     = ssh_connection_data.password
    address      = ssh_connection_data.host
    options      = r"-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
    safe_command = shlex.quote(command)
    ssh_command  = f"sshpass -p '{password}' ssh {username}@{address} {options} {safe_command}"
    return run_command(ssh_command)



