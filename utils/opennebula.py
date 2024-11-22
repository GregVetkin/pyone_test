import re

from utils      import run_command
from config     import RAFT_CONFIG





def restart_opennebula():
    # Иногда перезагрузка сервиса возвращает ненулевой код :(
    # Ребутим до победного, хоть вечность...
    while True:
        try:
            run_command("sudo systemctl restart opennebula")
            break
        except Exception:
            pass



def _get_federation_mode() -> str:
    content = run_command(f"sudo cat {RAFT_CONFIG}")
    
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
    
    content = run_command(f"sudo cat {RAFT_CONFIG}")
    
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

        run_command(f"sudo tee {RAFT_CONFIG} << EOF\n{content}\nEOF")
        
        restart_opennebula()


def federation_standalone():
    _change_federation_mode("STANDALONE")

def federation_master():
    _change_federation_mode("MASTER")

