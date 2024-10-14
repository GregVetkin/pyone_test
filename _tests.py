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
TESTS["one"]["system"]["version"]           = TestData(
                                                        xml_rpc_method  =   "one.system.version",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_version.py",
                                                        cli_command     =   "-"
)
TESTS["one"]["system"]["config"]            = TestData(
                                                        xml_rpc_method  =   "one.system.config",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_config.py",
                                                        cli_command     =   "-"
)
# =======================================================================================================================
# one.imagepool
TESTS["one"]["imagepool"] = {}
TESTS["one"]["imagepool"]["info"]           = TestData(
                                                        xml_rpc_method  =   "one.imagepool.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/imagepool/test_info.py",
                                                        cli_command     =   "oneimage list/top"
)
# =======================================================================================================================
# one.image
TESTS["one"]["image"] = {}
TESTS["one"]["image"]["persistent"]         = TestData(
                                                        xml_rpc_method  =   "one.image.persistent",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_persistent.py",
                                                        cli_command     =   "oneimage persistent/nonpersistent"
)
TESTS["one"]["image"]["enable"]             = TestData(
                                                        xml_rpc_method  =   "one.image.enable",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_enable.py",
                                                        cli_command     =   "oneimage enable/disable"
)
TESTS["one"]["image"]["chtype"]             = TestData(
                                                        xml_rpc_method  =   "one.image.chtype",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chtype.py",
                                                        cli_command     =   "oneimage chtype"
)
TESTS["one"]["image"]["snapshotdelete"]     = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotdelete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotdelete.py",
                                                        cli_command     =   "oneimage snapshot-delete*"
)
TESTS["one"]["image"]["snapshotrevert"]     = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotrevert",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotrevert.py",
                                                        cli_command     =   "oneimage snapshot-revert*"
)
TESTS["one"]["image"]["snapshotflatten"]    = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotflatten",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotflatten.py",
                                                        cli_command     =   "oneimage snapshot-flatten*"
)
TESTS["one"]["image"]["update"]             = TestData(
                                                        xml_rpc_method  =   "one.image.update",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_update.py",
                                                        cli_command     =   "oneimage update"
)
TESTS["one"]["image"]["allocate"]           = TestData(
                                                        xml_rpc_method  =   "one.image.allocate",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_allocate.py",
                                                        cli_command     =   "oneimage create"
)
TESTS["one"]["image"]["clone"]              = TestData(
                                                        xml_rpc_method  =   "one.image.clone",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_clone.py",
                                                        cli_command     =   "oneimage clone*"
)
TESTS["one"]["image"]["delete"]             = TestData(
                                                        xml_rpc_method  =   "one.image.delete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_delete.py",
                                                        cli_command     =   "oneimage delete*"
)
TESTS["one"]["image"]["info"]               = TestData(
                                                        xml_rpc_method  =   "one.image.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_info.py",
                                                        cli_command     =   "oneimage show"
)
TESTS["one"]["image"]["chown"]              = TestData(
                                                        xml_rpc_method  =   "one.image.chown",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chown.py",
                                                        cli_command     =   "oneimage chown/chgrp"
)
TESTS["one"]["image"]["chmod"]              = TestData(
                                                        xml_rpc_method  =   "one.image.chmod",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chmod.py",
                                                        cli_command     =   "oneimage chmod"
)
TESTS["one"]["image"]["rename"]             = TestData(
                                                        xml_rpc_method  =   "one.image.rename",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_rename.py",
                                                        cli_command     =   "oneimage rename"
)
TESTS["one"]["image"]["lock"]               = TestData(
                                                        xml_rpc_method  =   "one.image.lock",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_lock.py",
                                                        cli_command     =   "oneimage lock"
)
TESTS["one"]["image"]["unlock"]             = TestData(
                                                        xml_rpc_method  =   "one.image.unlock",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_unlock.py",
                                                        cli_command     =   "oneimage unlock"
)
TESTS["one"]["image"]["restore"]            = TestData(
                                                        xml_rpc_method  =   "one.image.restore",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_restore.py",
                                                        cli_command     =   "oneimage restore"
)
# =======================================================================================================================





