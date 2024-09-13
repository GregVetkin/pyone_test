import subprocess

from pathlib import Path

PROJECT_ROOT_PATH           = Path(__file__).resolve().parent.parent
ONEADMIN_TOKEN_SCRIPT_PATH  = f"{PROJECT_ROOT_PATH}/commands/create_oneadmin_token.sh"




def create_oneadmin_token():
    try:
        result = subprocess.run(
            ["bash", ONEADMIN_TOKEN_SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as err:
        print(err.stderr.strip())
        exit(1)

    else:
        return result.stdout.strip()



def create_token(username:str, group:str, exptime=3600) -> str:
    pass


def remove_token(username:str, group:str, exptime=3600) -> str:
    pass