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
# one.documents
TESTS["one"]["documents"] = {}
TESTS["one"]["documents"]["update"]     = ""
TESTS["one"]["documents"]["allocate"]   = ""
TESTS["one"]["documents"]["clone"]      = ""
TESTS["one"]["documents"]["delete"]     = ""
TESTS["one"]["documents"]["info"]       = ""
TESTS["one"]["documents"]["chown"]      = ""
TESTS["one"]["documents"]["chmod"]      = ""
TESTS["one"]["documents"]["rename"]     = ""
TESTS["one"]["documents"]["lock"]       = ""
TESTS["one"]["documents"]["unlock"]     = ""
TESTS["one"]["documents"]["info"]       = ""
# =======================================================================================================================



