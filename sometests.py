
import pyone
from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"aa62f54795822bf96e087f3e98b0d6d01136585c3e00df5cec1307dd17dce1b0"
# brestadm_auth = ADMIN_NAME+"~"+"Qwe!2345"

API_URI = "http://raft.brest.local:2633/RPC2"


# one = One(pyone.OneServer(API_URI, brestadm_auth))
# res = one.vm.action("resume", 18)
# print(res)


class ACL:
    class USERS:
        UID             =      0x100000000
        GID             =      0x200000000
        ALL             =      0x400000000
        CLUSTER         =      0x800000000

    class RESOURCES:
        VM              =     0x1000000000
        HOST            =     0x2000000000
        NET             =     0x4000000000
        IMAGE           =     0x8000000000
        USER            =    0x10000000000
        TEMPLATE        =    0x20000000000
        GROUP           =    0x40000000000
        DATASTORE       =   0x100000000000
        CLUSTER         =   0x200000000000
        DOCUMENT        =   0x400000000000
        ZONE            =   0x800000000000
        SECGROUP        =  0x1000000000000
        VDC             =  0x2000000000000
        VROUTER         =  0x4000000000000
        MARKETPLACE     =  0x8000000000000
        MARKETPLACEAPP  = 0x10000000000000
        VMGROUP         = 0x20000000000000
        VNTEMPLATE      = 0x40000000000000
        BACKUPJOB       =0x100000000000000

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




import base64

one = pyone.OneServer(API_URI, base64.b64encode(brestadm_auth.encode()).decode())
res = one.acl.addrule("400000000", "1400000000", "1", "100000005")
print(res)
