import re
import time
from utils.connection   import local_admin_ssh_conn
from utils.commands     import run_command_via_ssh
from config.base        import RAFT_CONFIG


def __run_command_via_ssh_as_local_admin(command: str):
    return run_command_via_ssh(local_admin_ssh_conn, command)





def __restart_opennebula_dopobednogo():
    # Иногда перезагрузка сервиса возвращает ненулевой код :(
    # Рестартим до победного, хоть вечность...
    while True:
        try:
            __run_command_via_ssh_as_local_admin("sudo systemctl restart opennebula")
            break
        except Exception:
            pass
    


def restart_opennebula(do_pobednogo: bool = True):
    if do_pobednogo:
        __restart_opennebula_dopobednogo()
    else:
        __run_command_via_ssh_as_local_admin("sudo systemctl restart opennebula")
    #sleep(5)
    




def _get_federation_mode() -> str:
    content = __run_command_via_ssh_as_local_admin(f"sudo cat {RAFT_CONFIG}")
    
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



def _change_federation_mode(mode: str) -> None:
    if _get_federation_mode() == mode:
        return
    
    content = __run_command_via_ssh_as_local_admin(f"sudo cat {RAFT_CONFIG}")
    
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

        __run_command_via_ssh_as_local_admin(f"sudo tee {RAFT_CONFIG} << EOF\n{content}\nEOF")
        
        restart_opennebula()


def federation_standalone():
    _change_federation_mode("STANDALONE")

def federation_master():
    _change_federation_mode("MASTER")

