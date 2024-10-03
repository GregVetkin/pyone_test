import os
from tests import TestData

# Текущий файл должен находиться в корне проекта
PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



# =======================================================================================================================
TESTS           = {}
TESTS["one"]    = {}
# =======================================================================================================================
# one.system
TESTS["one"]["system"] = {}
TESTS["one"]["system"]["version"]   = TestData(
        xml_rpc_method  =   "one.system.version",
        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_version.py",
        cli_command     =   "-"
    )
TESTS["one"]["system"]["config"]    = TestData(
        xml_rpc_method  =   "one.system.config",
        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_config.py",
        cli_command     =   "-"
    )
# =======================================================================================================================




