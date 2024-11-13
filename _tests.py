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
# one.datastorepool
TESTS["one"]["datastorepool"] = {}
TESTS["one"]["datastorepool"]["info"]       = TestData(
                                                        xml_rpc_method  =   "one.datastorepool.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastorepool/test_info.py"
)
# =======================================================================================================================
# one.datastore
TESTS["one"]["datastore"] = {}
TESTS["one"]["datastore"]["allocate"]       = TestData(
                                                        xml_rpc_method  =   "one.datastore.allocate",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_allocate.py"
)
TESTS["one"]["datastore"]["delete"]         = TestData(
                                                        xml_rpc_method  =   "one.datastore.delete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_delete.py"
)
TESTS["one"]["datastore"]["info"]           = TestData(
                                                        xml_rpc_method  =   "one.datastore.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_info.py"
)
TESTS["one"]["datastore"]["update"]         = TestData(
                                                        xml_rpc_method  =   "one.datastore.update",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_update.py"
)
TESTS["one"]["datastore"]["rename"]         = TestData(
                                                        xml_rpc_method  =   "one.datastore.rename",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_rename.py"
)
TESTS["one"]["datastore"]["chown"]          = TestData(
                                                        xml_rpc_method  =   "one.datastore.chown",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_chown.py"
)
TESTS["one"]["datastore"]["chmod"]          = TestData(
                                                        xml_rpc_method  =   "one.datastore.chmod",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_chmod.py"
)
TESTS["one"]["datastore"]["enable"]         = TestData(
                                                        xml_rpc_method  =   "one.datastore.enable",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/datastore/test_enable.py"
)
# =======================================================================================================================
# one.hostpool
TESTS["one"]["hostpool"] = {}
TESTS["one"]["hostpool"]["info"]            = TestData(
                                                        xml_rpc_method  =   "one.hostpool.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/hostpool/test_info.py"
)
# =======================================================================================================================
# one.host
TESTS["one"]["host"] = {}
TESTS["one"]["host"]["allocate"]            = TestData(
                                                        xml_rpc_method  =   "one.host.allocate",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_allocate.py"
)
TESTS["one"]["host"]["delete"]              = TestData(
                                                        xml_rpc_method  =   "one.host.delete",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_delete.py"
)
TESTS["one"]["host"]["info"]                = TestData(
                                                        xml_rpc_method  =   "one.host.info",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_info.py"                                    
)
TESTS["one"]["host"]["rename"]              = TestData(
                                                        xml_rpc_method  =   "one.host.rename",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_rename.py"
)
TESTS["one"]["host"]["update"]              = TestData(
                                                        xml_rpc_method  =   "one.host.update",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_update.py"
)
TESTS["one"]["host"]["status"]              = TestData(
                                                        xml_rpc_method  =   "one.host.status",
                                                        test_file_path  =   f"{PROJECT_DIR}/tests/host/test_status.py"                                    
)







# # =======================================================================================================================
# # one.acl
# TESTS["one"]["acl"] = {}
# TESTS["one"]["acl"]["addrule"]              = TestData(
#                                                         xml_rpc_method  =   "one.acl.addrule",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/acl/test_addrule.py"
# )
# TESTS["one"]["acl"]["delrule"]              = TestData(
#                                                         xml_rpc_method  =   "one.acl.delrule",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/acl/test_delrule.py"
# )
# TESTS["one"]["acl"]["info"]                 = TestData(
#                                                         xml_rpc_method  =   "one.acl.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/acl/test_info.py"
# )
# # =======================================================================================================================
# # one.cluster
# TESTS["one"]["cluster"] = {}
# TESTS["one"]["cluster"]["adddatastore"]     = TestData(
#                                                         xml_rpc_method  =   "one.cluster.adddatastore",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_adddatastore.py"
# )
# TESTS["one"]["cluster"]["addhost"]          = TestData(
#                                                         xml_rpc_method  =   "one.cluster.addhost",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_addhost.py"
# )
# TESTS["one"]["cluster"]["addvnet"]          = TestData(
#                                                         xml_rpc_method  =   "one.cluster.addvnet",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_addvnet.py"
# )
# TESTS["one"]["cluster"]["allocate"]         = TestData(
#                                                         xml_rpc_method  =   "one.cluster.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_allocate.py"
# )
# TESTS["one"]["cluster"]["deldatastore"]     = TestData(
#                                                         xml_rpc_method  =   "one.cluster.deldatastore",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_deldatastore.py"
# )
# TESTS["one"]["cluster"]["delete"]           = TestData(
#                                                         xml_rpc_method  =   "one.cluster.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_delete.py"
# )
# TESTS["one"]["cluster"]["delhost"]          = TestData(
#                                                         xml_rpc_method  =   "one.cluster.delhost",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_delhost.py"
# )
# TESTS["one"]["cluster"]["delvnet"]          = TestData(
#                                                         xml_rpc_method  =   "one.cluster.delvnet",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_delvnet.py"
# )
# TESTS["one"]["cluster"]["info"]             = TestData(
#                                                         xml_rpc_method  =   "one.cluster.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_info.py"
# )
# TESTS["one"]["cluster"]["rename"]           = TestData(
#                                                         xml_rpc_method  =   "one.cluster.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_rename.py"
# )
# TESTS["one"]["cluster"]["update"]           = TestData(
#                                                         xml_rpc_method  =   "one.cluster.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/cluster/test_update.py"
# )
# # =======================================================================================================================
# # one.clusterpool
# TESTS["one"]["clusterpool"] = {}
# TESTS["one"]["clusterpool"]["info"]         = TestData(
#                                                         xml_rpc_method  =   "one.clusterpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/clusterpool/test_info.py"
# )
# # =======================================================================================================================
# # one.document
# TESTS["one"]["document"] = {}
# TESTS["one"]["document"]["allocate"]        = TestData(
#                                                         xml_rpc_method  =   "one.document.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_allocate.py"
# )
# TESTS["one"]["document"]["chmod"]           = TestData(
#                                                         xml_rpc_method  =   "one.document.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_chmod.py"
# )
# TESTS["one"]["document"]["chown"]           = TestData(
#                                                         xml_rpc_method  =   "one.document.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_chown.py"
# )
# TESTS["one"]["document"]["clone"]           = TestData(
#                                                         xml_rpc_method  =   "one.document.clone",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_clone.py"
# )
# TESTS["one"]["document"]["delete"]          = TestData(
#                                                         xml_rpc_method  =   "one.document.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_delete.py"
# )
# TESTS["one"]["document"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.document.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_info.py"
# )
# TESTS["one"]["document"]["lock"]            = TestData(
#                                                         xml_rpc_method  =   "one.document.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_lock.py"
# )
# TESTS["one"]["document"]["rename"]          = TestData(
#                                                         xml_rpc_method  =   "one.document.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_rename.py"
# )
# TESTS["one"]["document"]["unlock"]          = TestData(
#                                                         xml_rpc_method  =   "one.document.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_unlock.py"
# )
# TESTS["one"]["document"]["update"]          = TestData(
#                                                         xml_rpc_method  =   "one.document.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/document/test_update.py"
# )
# # =======================================================================================================================
# # one.documentpool
# TESTS["one"]["documentpool"] = {}
# TESTS["one"]["documentpool"]["info"]        = TestData(
#                                                         xml_rpc_method  =   "one.documentpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/documentpool/test_info.py"
# )
# # =======================================================================================================================
# # one.group
# TESTS["one"]["group"] = {}
# TESTS["one"]["group"]["addadmin"]           = TestData(
#                                                         xml_rpc_method  =   "one.group.addadmin",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_addadmin.py"
# )
# TESTS["one"]["group"]["allocate"]           = TestData(
#                                                         xml_rpc_method  =   "one.group.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_allocate.py"
# )
# TESTS["one"]["group"]["deladmin"]           = TestData(
#                                                         xml_rpc_method  =   "one.group.deladmin",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_deladmin.py"
# )
# TESTS["one"]["group"]["delete"]             = TestData(
#                                                         xml_rpc_method  =   "one.group.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_delete.py"
# )
# TESTS["one"]["group"]["info"]               = TestData(
#                                                         xml_rpc_method  =   "one.group.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_info.py"
# )
# TESTS["one"]["group"]["quota"]              = TestData(
#                                                         xml_rpc_method  =   "one.group.quota",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_quota.py"
# )
# TESTS["one"]["group"]["update"]             = TestData(
#                                                         xml_rpc_method  =   "one.group.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/group/test_update.py"
# )
# # =======================================================================================================================
# # one.grouppool
# TESTS["one"]["grouppool"] = {}
# TESTS["one"]["grouppool"]["info"]           = TestData(
#                                                         xml_rpc_method  =   "one.grouppool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/grouppool/test_info.py"
# )
# # =======================================================================================================================
# # one.groupquota
# TESTS["one"]["groupquota"] = {}
# TESTS["one"]["groupquota"]["info"]          = TestData(
#                                                         xml_rpc_method  =   "one.groupquota.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/groupquota/test_info.py"
# )
# TESTS["one"]["groupquota"]["update"]        = TestData(
#                                                         xml_rpc_method  =   "one.groupquota.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/groupquota/test_update.py"
# )
# # =======================================================================================================================
# # one.hook
# TESTS["one"]["hook"] = {}
# TESTS["one"]["hook"]["allocate"]            = TestData(
#                                                         xml_rpc_method  =   "one.hook.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_allocate.py"
# )
# TESTS["one"]["hook"]["delete"]              = TestData(
#                                                         xml_rpc_method  =   "one.hook.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_delete.py"
# )
# TESTS["one"]["hook"]["info"]                = TestData(
#                                                         xml_rpc_method  =   "one.hook.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_info.py"
# )
# TESTS["one"]["hook"]["lock"]                = TestData(
#                                                         xml_rpc_method  =   "one.hook.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_lock.py"
# )
# TESTS["one"]["hook"]["rename"]              = TestData(
#                                                         xml_rpc_method  =   "one.hook.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_rename.py"
# )
# TESTS["one"]["hook"]["retry"]               = TestData(
#                                                         xml_rpc_method  =   "one.hook.retry",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_retry.py"
# )
# TESTS["one"]["hook"]["unlock"]              = TestData(
#                                                         xml_rpc_method  =   "one.hook.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_unlock.py"
# )
# TESTS["one"]["hook"]["update"]              = TestData(
#                                                         xml_rpc_method  =   "one.hook.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hook/test_update.py"
# )
# # =======================================================================================================================
# # one.hooklog
# TESTS["one"]["hooklog"] = {}
# TESTS["one"]["hooklog"]["info"]             = TestData(
#                                                         xml_rpc_method  =   "one.hooklog.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hooklog/test_info.py"
# )
# # =======================================================================================================================
# # one.hookpool
# TESTS["one"]["hookpool"] = {}
# TESTS["one"]["hookpool"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.hookpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/hookpool/test_info.py"
# )
# # =======================================================================================================================
# # one.market
# TESTS["one"]["market"] = {}
# TESTS["one"]["market"]["allocate"]          = TestData(
#                                                         xml_rpc_method  =   "one.market.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_allocate.py"
# )
# TESTS["one"]["market"]["chmod"]             = TestData(
#                                                         xml_rpc_method  =   "one.market.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_chmod.py"
# )
# TESTS["one"]["market"]["chown"]             = TestData(
#                                                         xml_rpc_method  =   "one.market.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_chown.py"
# )
# TESTS["one"]["market"]["delete"]            = TestData(
#                                                         xml_rpc_method  =   "one.market.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_delete.py"
# )
# TESTS["one"]["market"]["enable"]            = TestData(
#                                                         xml_rpc_method  =   "one.market.enable",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_enable.py"
# )
# TESTS["one"]["market"]["info"]              = TestData(
#                                                         xml_rpc_method  =   "one.market.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_info.py"
# )
# TESTS["one"]["market"]["rename"]            = TestData(
#                                                         xml_rpc_method  =   "one.market.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_rename.py"
# )
# TESTS["one"]["market"]["update"]            = TestData(
#                                                         xml_rpc_method  =   "one.market.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/market/test_update.py"
# )
# # =======================================================================================================================
# # one.marketapp
# TESTS["one"]["marketapp"] = {}
# TESTS["one"]["marketapp"]["allocate"]       = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_allocate.py"
# )
# TESTS["one"]["marketapp"]["chmod"]          = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_chmod.py"
# )
# TESTS["one"]["marketapp"]["chown"]          = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_chown.py"
# )
# TESTS["one"]["marketapp"]["delete"]         = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_delete.py"
# )
# TESTS["one"]["marketapp"]["enable"]         = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.enable",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_enable.py"
# )
# TESTS["one"]["marketapp"]["info"]           = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_info.py"
# )
# TESTS["one"]["marketapp"]["lock"]           = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_lock.py"
# )
# TESTS["one"]["marketapp"]["rename"]         = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_rename.py"
# )
# TESTS["one"]["marketapp"]["unlock"]         = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_unlock.py"
# )
# TESTS["one"]["marketapp"]["update"]         = TestData(
#                                                         xml_rpc_method  =   "one.marketapp.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapp/test_update.py"
# )
# # =======================================================================================================================
# # one.marketapppool
# TESTS["one"]["marketapppool"] = {}
# TESTS["one"]["marketapppool"]["info"]       = TestData(
#                                                         xml_rpc_method  =   "one.marketapppool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketapppool/test_info.py"
# )
# # =======================================================================================================================
# # one.marketpool
# TESTS["one"]["marketpool"] = {}
# TESTS["one"]["marketpool"]["info"]          = TestData(
#                                                         xml_rpc_method  =   "one.marketpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/marketpool/test_info.py"
# )
# # =======================================================================================================================
# # one.secgroup
# TESTS["one"]["secgroup"] = {}
# TESTS["one"]["secgroup"]["allocate"]        = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_allocate.py"
# )
# TESTS["one"]["secgroup"]["chmod"]           = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_chmod.py"
# )
# TESTS["one"]["secgroup"]["chown"]           = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_chown.py"
# )
# TESTS["one"]["secgroup"]["clone"]           = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.clone",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_clone.py"
# )
# TESTS["one"]["secgroup"]["commit"]          = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.commit",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_commit.py"
# )
# TESTS["one"]["secgroup"]["delete"]          = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_delete.py"
# )
# TESTS["one"]["secgroup"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_info.py"
# )
# TESTS["one"]["secgroup"]["rename"]          = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_rename.py"
# )
# TESTS["one"]["secgroup"]["update"]          = TestData(
#                                                         xml_rpc_method  =   "one.secgroup.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgroup/test_update.py"
# )
# # =======================================================================================================================
# # one.secgrouppoll
# TESTS["one"]["secgrouppoll"] = {}
# TESTS["one"]["secgrouppoll"]["info"]        = TestData(
#                                                         xml_rpc_method  =   "one.secgrouppoll.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/secgrouppoll/test_info.py"
# )
# # =======================================================================================================================
# # one.template
# TESTS["one"]["template"] = {}
# TESTS["one"]["template"]["allocate"]        = TestData(
#                                                         xml_rpc_method  =   "one.template.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_allocate.py"
# )
# TESTS["one"]["template"]["chmod"]           = TestData(
#                                                         xml_rpc_method  =   "one.template.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_chmod.py"
# )
# TESTS["one"]["template"]["chown"]           = TestData(
#                                                         xml_rpc_method  =   "one.template.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_chown.py"
# )
# TESTS["one"]["template"]["clone"]           = TestData(
#                                                         xml_rpc_method  =   "one.template.clone",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_clone.py"
# )
# TESTS["one"]["template"]["delete"]          = TestData(
#                                                         xml_rpc_method  =   "one.template.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_delete.py"
# )
# TESTS["one"]["template"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.template.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_info.py"
# )
# TESTS["one"]["template"]["instantiate"]     = TestData(
#                                                         xml_rpc_method  =   "one.template.instantiate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_instantiate.py"
# )
# TESTS["one"]["template"]["lock"]            = TestData(
#                                                         xml_rpc_method  =   "one.template.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_lock.py"
# )
# TESTS["one"]["template"]["rename"]          = TestData(
#                                                         xml_rpc_method  =   "one.template.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_rename.py"
# )
# TESTS["one"]["template"]["unlock"]          = TestData(
#                                                         xml_rpc_method  =   "one.template.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_unlock.py"
# )
# TESTS["one"]["template"]["update"]          = TestData(
#                                                         xml_rpc_method  =   "one.template.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/template/test_update.py"
# )
# # =======================================================================================================================
# # one.templatepool
# TESTS["one"]["templatepool"] = {}
# TESTS["one"]["templatepool"]["info"]        = TestData(
#                                                         xml_rpc_method  =   "one.templatepool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/templatepool/test_info.py"
# )
# # =======================================================================================================================
# # one.user
# TESTS["one"]["user"] = {}
# TESTS["one"]["user"]["addgroup"]            = TestData(
#                                                         xml_rpc_method  =   "one.user.addgroup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_addgroup.py"
# )
# TESTS["one"]["user"]["allocate"]            = TestData(
#                                                         xml_rpc_method  =   "one.user.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_allocate.py"
# )
# TESTS["one"]["user"]["chauth"]              = TestData(
#                                                         xml_rpc_method  =   "one.user.chauth",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_chauth.py"
# )
# TESTS["one"]["user"]["chgrp"]               = TestData(
#                                                         xml_rpc_method  =   "one.user.chgrp",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_chgrp.py"
# )
# TESTS["one"]["user"]["delete"]              = TestData(
#                                                         xml_rpc_method  =   "one.user.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_delete.py"
# )
# TESTS["one"]["user"]["delgroup"]            = TestData(
#                                                         xml_rpc_method  =   "one.user.delgroup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_delgroup.py"
# )
# TESTS["one"]["user"]["enable"]              = TestData(
#                                                         xml_rpc_method  =   "one.user.enable",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_enable.py"
# )
# TESTS["one"]["user"]["info"]                = TestData(
#                                                         xml_rpc_method  =   "one.user.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_info.py"
# )
# TESTS["one"]["user"]["login"]               = TestData(
#                                                         xml_rpc_method  =   "one.user.login",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_login.py"
# )
# TESTS["one"]["user"]["passwd"]              = TestData(
#                                                         xml_rpc_method  =   "one.user.passwd",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_passwd.py"
# )
# TESTS["one"]["user"]["quota"]               = TestData(
#                                                         xml_rpc_method  =   "one.user.quota",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_quota.py"
# )
# TESTS["one"]["user"]["update"]              = TestData(
#                                                         xml_rpc_method  =   "one.user.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/user/test_update.py"
# )
# # =======================================================================================================================
# # one.userpool
# TESTS["one"]["userpool"] = {}
# TESTS["one"]["userpool"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.userpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/userpool/test_info.py"
# )
# # =======================================================================================================================
# # one.userquota
# TESTS["one"]["userquota"] = {}
# TESTS["one"]["userquota"]["info"]           = TestData(
#                                                         xml_rpc_method  =   "one.userquota.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/userquota/test_info.py"
# )
# TESTS["one"]["userquota"]["update"]         = TestData(
#                                                         xml_rpc_method  =   "one.userquota.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/userquota/test_update.py"
# )
# # =======================================================================================================================
# # one.vdc
# TESTS["one"]["vdc"] = {}
# TESTS["one"]["vdc"]["addcluster"]           = TestData(
#                                                         xml_rpc_method  =   "one.vdc.addcluster",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_addcluster.py"
# )
# TESTS["one"]["vdc"]["adddatastore"]         = TestData(
#                                                         xml_rpc_method  =   "one.vdc.adddatastore",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_adddatastore.py"
# )
# TESTS["one"]["vdc"]["addgroup"]             = TestData(
#                                                         xml_rpc_method  =   "one.vdc.addgroup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_addgroup.py"
# )
# TESTS["one"]["vdc"]["addhost"]              = TestData(
#                                                         xml_rpc_method  =   "one.vdc.addhost",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_addhost.py"
# )
# TESTS["one"]["vdc"]["addvnet"]              = TestData(
#                                                         xml_rpc_method  =   "one.vdc.addvnet",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_addvnet.py"
# )
# TESTS["one"]["vdc"]["allocate"]             = TestData(
#                                                         xml_rpc_method  =   "one.vdc.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_allocate.py"
# )
# TESTS["one"]["vdc"]["delcluster"]           = TestData(
#                                                         xml_rpc_method  =   "one.vdc.delcluster",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_delcluster.py"
# )
# TESTS["one"]["vdc"]["deldatastore"]         = TestData(
#                                                         xml_rpc_method  =   "one.vdc.deldatastore",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_deldatastore.py"
# )
# TESTS["one"]["vdc"]["delete"]               = TestData(
#                                                         xml_rpc_method  =   "one.vdc.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_delete.py"
# )
# TESTS["one"]["vdc"]["delgroup"]             = TestData(
#                                                         xml_rpc_method  =   "one.vdc.delgroup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_delgroup.py"
# )
# TESTS["one"]["vdc"]["delhost"]              = TestData(
#                                                         xml_rpc_method  =   "one.vdc.delhost",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_delhost.py"
# )
# TESTS["one"]["vdc"]["delvnet"]              = TestData(
#                                                         xml_rpc_method  =   "one.vdc.delvnet",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_delvnet.py"
# )
# TESTS["one"]["vdc"]["info"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vdc.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_info.py"
# )
# TESTS["one"]["vdc"]["rename"]               = TestData(
#                                                         xml_rpc_method  =   "one.vdc.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_rename.py"
# )
# TESTS["one"]["vdc"]["update"]               = TestData(
#                                                         xml_rpc_method  =   "one.vdc.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdc/test_update.py"
# )
# # =======================================================================================================================
# # one.vdcpool
# TESTS["one"]["vdcpool"] = {}
# TESTS["one"]["vdcpool"]["info"]             = TestData(
#                                                         xml_rpc_method  =   "one.vdcpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vdcpool/test_info.py"
# )
# # =======================================================================================================================
# # one.vm
# TESTS["one"]["vm"] = {}
# TESTS["one"]["vm"]["action"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.action",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_action.py"
# )
# TESTS["one"]["vm"]["allocate"]              = TestData(
#                                                         xml_rpc_method  =   "one.vm.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_allocate.py"
# )
# TESTS["one"]["vm"]["attach"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.attach",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_attach.py"
# )
# TESTS["one"]["vm"]["attachnic"]             = TestData(
#                                                         xml_rpc_method  =   "one.vm.attachnic",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_attachnic.py"
# )
# TESTS["one"]["vm"]["attachpci"]             = TestData(
#                                                         xml_rpc_method  =   "one.vm.attachpci",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_attachpci.py"
# )
# TESTS["one"]["vm"]["attachsg"]              = TestData(
#                                                         xml_rpc_method  =   "one.vm.attachsg",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_attachsg.py"
# )
# TESTS["one"]["vm"]["backup"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.backup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_backup.py"
# )
# TESTS["one"]["vm"]["backup"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.backup",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_backup.py"
# )
# TESTS["one"]["vm"]["backupcancel"]          = TestData(
#                                                         xml_rpc_method  =   "one.vm.backupcancel",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_backupcancel.py"
# )
# TESTS["one"]["vm"]["chmod"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vm.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_chmod.py"
# )
# TESTS["one"]["vm"]["chown"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vm.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_chown.py"
# )
# TESTS["one"]["vm"]["deploy"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.deploy",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_deploy.py"
# )
# TESTS["one"]["vm"]["detach"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.detach",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_detach.py"
# )
# TESTS["one"]["vm"]["detachnic"]             = TestData(
#                                                         xml_rpc_method  =   "one.vm.detachnic",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_detachnic.py"
# )
# TESTS["one"]["vm"]["detachpci"]             = TestData(
#                                                         xml_rpc_method  =   "one.vm.detachpci",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_detachpci.py"
# )
# TESTS["one"]["vm"]["detachsg"]              = TestData(
#                                                         xml_rpc_method  =   "one.vm.detachsg",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_detachsg.py"
# )
# TESTS["one"]["vm"]["diskresize"]            = TestData(
#                                                         xml_rpc_method  =   "one.vm.diskresize",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_diskresize.py"
# )
# TESTS["one"]["vm"]["disksaveas"]            = TestData(
#                                                         xml_rpc_method  =   "one.vm.disksaveas",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_disksaveas.py"
# )
# TESTS["one"]["vm"]["disksnapshotcreate"]    = TestData(
#                                                         xml_rpc_method  =   "one.vm.disksnapshotcreate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_disksnapshotcreate.py"
# )
# TESTS["one"]["vm"]["disksnapshotdelete"]    = TestData(
#                                                         xml_rpc_method  =   "one.vm.disksnapshotdelete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_disksnapshotdelete.py"
# )
# TESTS["one"]["vm"]["disksnapshotrename"]    = TestData(
#                                                         xml_rpc_method  =   "one.vm.disksnapshotrename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_disksnapshotrename.py"
# )
# TESTS["one"]["vm"]["disksnapshotrevert"]    = TestData(
#                                                         xml_rpc_method  =   "one.vm.disksnapshotrevert",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_disksnapshotrevert.py"
# )
# TESTS["one"]["vm"]["info"]                  = TestData(
#                                                         xml_rpc_method  =   "one.vm.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_info.py"
# )
# TESTS["one"]["vm"]["lock"]                  = TestData(
#                                                         xml_rpc_method  =   "one.vm.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_lock.py"
# )
# TESTS["one"]["vm"]["migrate"]               = TestData(
#                                                         xml_rpc_method  =   "one.vm.migrate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_migrate.py"
# )
# TESTS["one"]["vm"]["monitoring"]            = TestData(
#                                                         xml_rpc_method  =   "one.vm.monitoring",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_monitoring.py"
# )
# TESTS["one"]["vm"]["recover"]               = TestData(
#                                                         xml_rpc_method  =   "one.vm.recover",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_recover.py"
# )
# TESTS["one"]["vm"]["rename"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_rename.py"
# )
# TESTS["one"]["vm"]["resize"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.resize",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_resize.py"
# )
# TESTS["one"]["vm"]["schedadd"]              = TestData(
#                                                         xml_rpc_method  =   "one.vm.schedadd",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_schedadd.py"
# )
# TESTS["one"]["vm"]["scheddelete"]           = TestData(
#                                                         xml_rpc_method  =   "one.vm.scheddelete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_scheddelete.py"
# )
# TESTS["one"]["vm"]["schedupdate"]           = TestData(
#                                                         xml_rpc_method  =   "one.vm.schedupdate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_schedupdate.py"
# )
# TESTS["one"]["vm"]["snapshotcreate"]        = TestData(
#                                                         xml_rpc_method  =   "one.vm.snapshotcreate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_snapshotcreate.py"
# )
# TESTS["one"]["vm"]["snapshotdelete"]        = TestData(
#                                                         xml_rpc_method  =   "one.vm.snapshotdelete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_snapshotdelete.py"
# )
# TESTS["one"]["vm"]["snapshotrevert"]        = TestData(
#                                                         xml_rpc_method  =   "one.vm.snapshotrevert",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_snapshotrevert.py"
# )
# TESTS["one"]["vm"]["unlock"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_unlock.py"
# )
# TESTS["one"]["vm"]["update"]                = TestData(
#                                                         xml_rpc_method  =   "one.vm.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_update.py"
# )
# TESTS["one"]["vm"]["updateconf"]            = TestData(
#                                                         xml_rpc_method  =   "one.vm.updateconf",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_updateconf.py"
# )
# TESTS["one"]["vm"]["updatenic"]             = TestData(
#                                                         xml_rpc_method  =   "one.vm.updatenic",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vm/test_updatenic.py"
# )
# # =======================================================================================================================
# # one.vmgroup
# TESTS["one"]["vmgroup"] = {}
# TESTS["one"]["vmgroup"]["allocate"]         = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_allocate.py"
# )
# TESTS["one"]["vmgroup"]["chmod"]            = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_chmod.py"
# )
# TESTS["one"]["vmgroup"]["chown"]            = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_chown.py"
# )
# TESTS["one"]["vmgroup"]["delete"]           = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_delete.py"
# )
# TESTS["one"]["vmgroup"]["info"]             = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_info.py"
# )
# TESTS["one"]["vmgroup"]["lock"]             = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_lock.py"
# )
# TESTS["one"]["vmgroup"]["rename"]           = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_rename.py"
# )
# TESTS["one"]["vmgroup"]["unlock"]           = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_unlock.py"
# )
# TESTS["one"]["vmgroup"]["update"]           = TestData(
#                                                         xml_rpc_method  =   "one.vmgroup.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgroup/test_update.py"
# )
# # =======================================================================================================================
# # one.vmgrouppool
# TESTS["one"]["vmgrouppool"] = {}
# TESTS["one"]["vmgrouppool"]["info"]         = TestData(
#                                                         xml_rpc_method  =   "one.vmgrouppool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmgrouppool/test_info.py"
# )
# # =======================================================================================================================
# # one.vmpool
# TESTS["one"]["vmpool"] = {}
# TESTS["one"]["vmpool"]["accounting"]        = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.accounting",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_accounting.py"
# )
# TESTS["one"]["vmpool"]["calculateshowback"] = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.calculateshowback",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_calculateshowback.py"
# )
# TESTS["one"]["vmpool"]["info"]              = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_info.py"
# )
# TESTS["one"]["vmpool"]["infoextended"]      = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.infoextended",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_infoextended.py"
# )
# TESTS["one"]["vmpool"]["infoset"]           = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.infoset",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_infoset.py"
# )
# TESTS["one"]["vmpool"]["monitoring"]        = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.monitoring",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_monitoring.py"
# )
# TESTS["one"]["vmpool"]["showback"]          = TestData(
#                                                         xml_rpc_method  =   "one.vmpool.showback",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vmpool/test_showback.py"
# )
# # =======================================================================================================================
# # one.vn
# TESTS["one"]["vn"] = {}
# TESTS["one"]["vn"]["add_ar"]                = TestData(
#                                                         xml_rpc_method  =   "one.vn.add_ar",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_add_ar.py"
# )
# TESTS["one"]["vn"]["allocate"]              = TestData(
#                                                         xml_rpc_method  =   "one.vn.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_allocate.py"
# )
# TESTS["one"]["vn"]["chmod"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vn.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_chmod.py"
# )
# TESTS["one"]["vn"]["chown"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vn.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_chown.py"
# )
# TESTS["one"]["vn"]["delete"]                = TestData(
#                                                         xml_rpc_method  =   "one.vn.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_delete.py"
# )
# TESTS["one"]["vn"]["free_ar"]               = TestData(
#                                                         xml_rpc_method  =   "one.vn.free_ar",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_free_ar.py"
# )
# TESTS["one"]["vn"]["hold"]                  = TestData(
#                                                         xml_rpc_method  =   "one.vn.hold",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_hold.py"
# )
# TESTS["one"]["vn"]["info"]                  = TestData(
#                                                         xml_rpc_method  =   "one.vn.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_info.py"
# )
# TESTS["one"]["vn"]["lock"]                  = TestData(
#                                                         xml_rpc_method  =   "one.vn.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_lock.py"
# )
# TESTS["one"]["vn"]["recover"]               = TestData(
#                                                         xml_rpc_method  =   "one.vn.recover",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_recover.py"
# )
# TESTS["one"]["vn"]["release"]               = TestData(
#                                                         xml_rpc_method  =   "one.vn.release",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_release.py"
# )
# TESTS["one"]["vn"]["rename"]                = TestData(
#                                                         xml_rpc_method  =   "one.vn.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_rename.py"
# )
# TESTS["one"]["vn"]["reserve"]               = TestData(
#                                                         xml_rpc_method  =   "one.vn.reserve",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_reserve.py"
# )
# TESTS["one"]["vn"]["rm_ar"]                 = TestData(
#                                                         xml_rpc_method  =   "one.vn.rm_ar",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_rm_ar.py"
# )
# TESTS["one"]["vn"]["unlock"]                = TestData(
#                                                         xml_rpc_method  =   "one.vn.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_unlock.py"
# )
# TESTS["one"]["vn"]["update_ar"]             = TestData(
#                                                         xml_rpc_method  =   "one.vn.update_ar",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_update_ar.py"
# )
# TESTS["one"]["vn"]["update"]                = TestData(
#                                                         xml_rpc_method  =   "one.vn.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vn/test_update.py"
# )
# # =======================================================================================================================
# # one.vnpool
# TESTS["one"]["vnpool"] = {}
# TESTS["one"]["vnpool"]["info"]              = TestData(
#                                                         xml_rpc_method  =   "one.vnpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vnpool/test_info.py"
# )
# # =======================================================================================================================
# # one.vntemplate
# TESTS["one"]["vntemplate"] = {}
# TESTS["one"]["vntemplate"]["allocate"]      = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_allocate.py"
# )
# TESTS["one"]["vntemplate"]["chmod"]         = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_chmod.py"
# )
# TESTS["one"]["vntemplate"]["chown"]         = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_chown.py"
# )
# TESTS["one"]["vntemplate"]["clone"]         = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.clone",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_clone.py"
# )
# TESTS["one"]["vntemplate"]["delete"]        = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_delete.py"
# )
# TESTS["one"]["vntemplate"]["info"]          = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_info.py"
# )
# TESTS["one"]["vntemplate"]["instantiate"]   = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.instantiate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_instantiate.py"
# )
# TESTS["one"]["vntemplate"]["lock"]          = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_lock.py"
# )
# TESTS["one"]["vntemplate"]["rename"]        = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_rename.py"
# )
# TESTS["one"]["vntemplate"]["unlock"]        = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_unlock.py"
# )
# TESTS["one"]["vntemplate"]["update"]        = TestData(
#                                                         xml_rpc_method  =   "one.vntemplate.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplate/test_update.py"
# )
# # =======================================================================================================================
# # one.vntemplatepool
# TESTS["one"]["vntemplatepool"] = {}
# TESTS["one"]["vntemplatepool"]["info"]      = TestData(
#                                                         xml_rpc_method  =   "one.vntemplatepool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vntemplatepool/test_info.py"
# )
# # =======================================================================================================================
# # one.vntemplatepool
# TESTS["one"]["vrouter"] = {}
# TESTS["one"]["vrouter"]["allocate"]         = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_allocate.py"
# )
# TESTS["one"]["vrouter"]["attachnic"]        = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.attachnic",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_attachnic.py"
# )
# TESTS["one"]["vrouter"]["chmod"]            = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.chmod",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_chmod.py"
# )
# TESTS["one"]["vrouter"]["chown"]            = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.chown",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_chown.py"
# )
# TESTS["one"]["vrouter"]["delete"]           = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_delete.py"
# )
# TESTS["one"]["vrouter"]["detachnic"]        = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.detachnic",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_detachnic.py"
# )
# TESTS["one"]["vrouter"]["info"]             = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_info.py"
# )
# TESTS["one"]["vrouter"]["instantiate"]      = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.instantiate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_instantiate.py"
# )
# TESTS["one"]["vrouter"]["lock"]             = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.lock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_lock.py"
# )
# TESTS["one"]["vrouter"]["rename"]           = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_rename.py"
# )
# TESTS["one"]["vrouter"]["unlock"]           = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.unlock",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_unlock.py"
# )
# TESTS["one"]["vrouter"]["update"]           = TestData(
#                                                         xml_rpc_method  =   "one.vrouter.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouter/test_update.py"
# )
# # =======================================================================================================================
# # one.vrouterpool
# TESTS["one"]["vrouterpool"] = {}
# TESTS["one"]["vrouterpool"]["info"]         = TestData(
#                                                         xml_rpc_method  =   "one.vrouterpool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/vrouterpool/test_info.py"
# )
# # =======================================================================================================================
# # one.zone
# TESTS["one"]["zone"] = {}
# TESTS["one"]["zone"]["allocate"]            = TestData(
#                                                         xml_rpc_method  =   "one.zone.allocate",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_allocate.py"
# )
# TESTS["one"]["zone"]["delete"]              = TestData(
#                                                         xml_rpc_method  =   "one.zone.delete",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_delete.py"
# )
# TESTS["one"]["zone"]["enable"]              = TestData(
#                                                         xml_rpc_method  =   "one.zone.enable",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_enable.py"
# )
# TESTS["one"]["zone"]["info"]                = TestData(
#                                                         xml_rpc_method  =   "one.zone.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_info.py"
# )
# TESTS["one"]["zone"]["raftstatus"]          = TestData(
#                                                         xml_rpc_method  =   "one.zone.raftstatus",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_raftstatus.py"
# )
# TESTS["one"]["zone"]["rename"]              = TestData(
#                                                         xml_rpc_method  =   "one.zone.rename",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_rename.py"
# )
# TESTS["one"]["zone"]["update"]              = TestData(
#                                                         xml_rpc_method  =   "one.zone.update",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zone/test_update.py"
# )
# # =======================================================================================================================
# # one.zonepool
# TESTS["one"]["zonepool"] = {}
# TESTS["one"]["zonepool"]["info"]            = TestData(
#                                                         xml_rpc_method  =   "one.zonepool.info",
#                                                         test_file_path  =   f"{PROJECT_DIR}/tests/zonepool/test_info.py"
# )
