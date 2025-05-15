import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

ALSE_VERSION        = 1.8
BREST_VERSION       = 4

API_URI             = "http://bufn1.brest.local:2633/RPC2"
RAFT_API_URI        = "http://10.0.70.20:2633/RPC2"

ADMIN_NAME          = "brestadm"
ADMIN_PASSWORD      = "Qwe!2345"

BAD_SYMBOLS         = ['$', '#', '&', '\"', '\'', '>', '<', '/', '\\', '|']
LOCK_LEVELS         = [1, 2, 3, 4]


RAFT_CONFIG         = "/etc/one/one.d/raft.conf"








# Virtual Machine states
# https://wiki.astralinux.ru/brest/3.2/statusy-vm-v-pk-sv-brest-311346813.html

class VmStates:
    INIT            = 0
    PENDING         = 1
    HOLD            = 2
    ACTIVE          = 3
    STOPPED         = 4
    SUSPENDED       = 5
    DONE            = 6
    POWEROFF        = 8
    UNDEPLOYED      = 9
    CLONING         = 10
    CLONING_FAILURE = 11

class VmLcmStates:
    LCM_INIT                        = 0
    PROLOG                          = 1
    BOOT                            = 2
    RUNNING                         = 3
    MIGRATE                         = 4
    SAVE_STOP                       = 5
    SAVE_SUSPEND                    = 6
    SAVE_MIGRATE                    = 7 
    PROLOG_MIGRATE                  = 8
    PROLOG_RESUME                   = 9
    EPILOG_STOP                     = 10
    EPILOG                          = 11
    SHUTDOWN                        = 12
    CLEANUP_RESUBMIT                = 15
    UNKNOWN                         = 16
    HOTPLUG                         = 17
    SHUTDOWN_POWEROFF               = 18
    BOOT_UNKNOWN                    = 19
    BOOT_POWEROFF                   = 20
    BOOT_SUSPENDED                  = 21
    BOOT_STOPPED                    = 22
    CLEANUP_DELETE                  = 23
    HOTPLUG_SNAPSHOT                = 24
    HOTPLUG_NIC                     = 25
    HOTPLUG_SAVEAS                  = 26
    HOTPLUG_SAVEAS_POWEROFF         = 27
    HOTPLUG_SAVEAS_SUSPENDED        = 28
    SHUTDOWN_UNDEPLOY               = 29
    EPILOG_UNDEPLOY                 = 30
    PROLOG_UNDEPLOY                 = 31
    BOOT_UNDEPLOY                   = 32
    HOTPLUG_PROLOG_POWEROFF         = 33
    HOTPLUG_EPILOG_POWEROFF         = 34
    BOOT_MIGRATE                    = 35
    BOOT_FAILURE                    = 36
    BOOT_MIGRATE_FAILURE            = 37
    PROLOG_MIGRATE_FAILURE          = 38
    PROLOG_FAILURE                  = 39
    EPILOG_FAILURE                  = 40
    EPILOG_STOP_FAILURE             = 41
    EPILOG_UNDEPLOY_FAILURE         = 42
    PROLOG_MIGRATE_POWEROFF         = 43
    PROLOG_MIGRATE_POWEROFF_FAILURE = 44
    PROLOG_MIGRATE_SUSPEND          = 45
    PROLOG_MIGRATE_SUSPEND_FAILURE  = 46
    BOOT_UNDEPLOY_FAILURE           = 47
    BOOT_STOPPED_FAILURE            = 48
    PROLOG_RESUME_FAILURE           = 49
    PROLOG_UNDEPLOY_FAILURE         = 50
    DISK_SNAPSHOT_POWEROFF          = 51
    DISK_SNAPSHOT_REVERT_POWEROFF   = 52
    DISK_SNAPSHOT_DELETE_POWEROFF   = 53
    DISK_SNAPSHOT_SUSPENDED         = 54
    DISK_SNAPSHOT_REVERT_SUSPENDED  = 55
    DISK_SNAPSHOT_DELETE_SUSPENDED  = 56
    DISK_SNAPSHOT                   = 57
    DISK_SNAPSHOT_DELETE            = 59
    PROLOG_MIGRATE_UNKNOWN          = 60
    PROLOG_MIGRATE_UNKNOWN_FAILURE  = 61
    DISK_RESIZE                     = 62
    DISK_RESIZE_POWEROFF            = 63
    DISK_RESIZE_UNDEPLOYED          = 64
    HOTPLUG_NIC_POWEROFF            = 65
    HOTPLUG_RESIZE                  = 66
    HOTPLUG_SAVEAS_UNDEPLOYED       = 67
    HOTPLUG_SAVEAS_STOPPED          = 68
    BACKUP                          = 69
    BACKUP_POWEROFF                 = 70
    RESTORE                         = 71
