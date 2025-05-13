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



class VmActions:
    TERMINATE_HARD  = "terminate-hard"
    TERMINATE       = "terminate"
    UNDEPLOY_HARD   = "undeploy-hard"
    UNDEPLOY        = "undeploy"
    POWEROFF_HARD   = "poweroff-hard"
    POWEROFF        = "poweroff"
    REBOOT_HARD     = "reboot-hard"
    REBOOT          = "reboot"
    HOLD            = "hold"
    RELEASE         = "release"
    STOP            = "stop"
    SUSPEND         = "suspend"
    RESUME          = "resume"
    RESCHED         = "resched"
    UNRESCHED       = "unresched"


class VmRecoverOperations:
    FAILURE         = 0
    SUCCESS         = 1
    RETRY           = 2
    DELETE          = 3
    DELETE_RECREATE = 4
    DELETE_DB       = 5



class ImageStates:
    INIT                = 0
    READY               = 1
    USED                = 2
    DISABLED            = 3
    LOCKED              = 4
    ERROR               = 5
    CLONE               = 6
    DELETE              = 7
    USED_PERS           = 8
    LOCKED_USED         = 9
    LOCKED_USED_PERS    = 10



class DatastoreTypes:
    IMAGE   = 0
    SYSTEM  = 1
    FILE    = 2



class HostStates:
    INIT                    = 0
    MONITORING_MONITORED    = 1
    ENABLED                 = 2
    ERROR                   = 3
    DISABLED                = 4
    MONITORING_ERROR        = 5
    MONITORING_INIT         = 6
    MONITORING_DISABLED     = 7
    OFFLINE                 = 8





class ACL:
    class USERS:
        UID             =       0x100000000
        GID             =       0x200000000
        ALL             =       0x400000000
        CLUSTER         =       0x800000000

    class RESOURCES:
        VM              =      0x1000000000
        HOST            =      0x2000000000
        NET             =      0x4000000000
        IMAGE           =      0x8000000000
        USER            =     0x10000000000
        TEMPLATE        =     0x20000000000
        GROUP           =     0x40000000000
        DATASTORE       =    0x100000000000
        CLUSTER         =    0x200000000000
        DOCUMENT        =    0x400000000000
        ZONE            =    0x800000000000
        SECGROUP        =   0x1000000000000
        VDC             =   0x2000000000000
        VROUTER         =   0x4000000000000
        MARKETPLACE     =   0x8000000000000
        MARKETPLACEAPP  =  0x10000000000000
        VMGROUP         =  0x20000000000000
        VNTEMPLATE      =  0x40000000000000
        BACKUPJOB       = 0x100000000000000

    class RIGHTS:
        USE             = 0x1
        MANAGE          = 0x2
        ADMIN           = 0x4
        CREATE          = 0x8

    def _number_to_hex_string(number):
        return f"{number:x}"

    @classmethod
    def applies_to_all(cls):
        return cls._number_to_hex_string(cls.USERS.ALL)


