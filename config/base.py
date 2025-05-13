import os

ASTRA_VERSION           = "1.8"
BREST_VERSION           = "4.0"
DOMAIN_NAME             = "brest.local"
RAFT_ENABLED            = False


RAFT_NODE_ADDRESS       = "10.0.70.20"
SOLO_NODE_ADDRESS       = "10.0.70.21"
API_URI                 = f"http://{RAFT_NODE_ADDRESS if RAFT_ENABLED else SOLO_NODE_ADDRESS}:2633/RPC2"


RAFT_CONFIG             = "/etc/one/one.d/raft.conf"




PROJECT_DIRECTORY       = os.path.dirname(os.path.abspath(__file__))
SHELL_SCRIPTS_PATH      = os.path.join(PROJECT_DIRECTORY,   "shell")
PREPARE_SCRIPT_PATH     = os.path.join(SHELL_SCRIPTS_PATH,  "prepare_venv.sh")
VENV_DIRECTORY_PATH     = os.path.join(PROJECT_DIRECTORY,   ".venv")
VENV_PYTHON_3_PATH      = os.path.join(VENV_DIRECTORY_PATH, "bin/python3")
TESTS_DIRECTORY_PATH    = os.path.join(PROJECT_DIRECTORY,   "tests")



class LocalAdmin:
    USERNAME = "u"
    PASSWORD = "1"


class BrestAdmin:
    USERNAME = "brestadm"
    PASSWORD = "Qwe!2345"
