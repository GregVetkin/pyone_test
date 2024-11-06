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
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_version.py"
)
TESTS["one"]["system"]["config"]            = TestData(
                                                        xml_rpc_method  =   "one.system.config",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/system/test_config.py"
)
# =======================================================================================================================
# one.imagepool
TESTS["one"]["imagepool"] = {}
TESTS["one"]["imagepool"]["info"]           = TestData(
                                                        xml_rpc_method  =   "one.imagepool.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/imagepool/test_info.py"
)
# =======================================================================================================================
# one.image
TESTS["one"]["image"] = {}
TESTS["one"]["image"]["persistent"]         = TestData(
                                                        xml_rpc_method  =   "one.image.persistent",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_persistent.py"
)
TESTS["one"]["image"]["enable"]             = TestData(
                                                        xml_rpc_method  =   "one.image.enable",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_enable.py"
)
TESTS["one"]["image"]["chtype"]             = TestData(
                                                        xml_rpc_method  =   "one.image.chtype",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chtype.py"
)
TESTS["one"]["image"]["snapshotdelete"]     = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotdelete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotdelete.py"
)
TESTS["one"]["image"]["snapshotrevert"]     = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotrevert",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotrevert.py"
)
TESTS["one"]["image"]["snapshotflatten"]    = TestData(
                                                        xml_rpc_method  =   "one.image.snapshotflatten",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_snapshotflatten.py"
)
TESTS["one"]["image"]["update"]             = TestData(
                                                        xml_rpc_method  =   "one.image.update",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_update.py"
)
TESTS["one"]["image"]["allocate"]           = TestData(
                                                        xml_rpc_method  =   "one.image.allocate",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_allocate.py"
)
TESTS["one"]["image"]["clone"]              = TestData(
                                                        xml_rpc_method  =   "one.image.clone",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_clone.py"
)
TESTS["one"]["image"]["delete"]             = TestData(
                                                        xml_rpc_method  =   "one.image.delete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_delete.py"
)
TESTS["one"]["image"]["info"]               = TestData(
                                                        xml_rpc_method  =   "one.image.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_info.py"
)
TESTS["one"]["image"]["chown"]              = TestData(
                                                        xml_rpc_method  =   "one.image.chown",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chown.py"
)
TESTS["one"]["image"]["chmod"]              = TestData(
                                                        xml_rpc_method  =   "one.image.chmod",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_chmod.py"
)
TESTS["one"]["image"]["rename"]             = TestData(
                                                        xml_rpc_method  =   "one.image.rename",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_rename.py"
)
TESTS["one"]["image"]["lock"]               = TestData(
                                                        xml_rpc_method  =   "one.image.lock",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_lock.py"
)
TESTS["one"]["image"]["unlock"]             = TestData(
                                                        xml_rpc_method  =   "one.image.unlock",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_unlock.py"
)
TESTS["one"]["image"]["restore"]            = TestData(
                                                        xml_rpc_method  =   "one.image.restore",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/image/test_restore.py"
)
# =======================================================================================================================





