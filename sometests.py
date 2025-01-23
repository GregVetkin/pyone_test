import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"fa20ef55f090e3e00980a25b2f3876725b4aa6c6d32239410c802e5912487715"


# one = pyone.OneServer(API_URI, brestadm_auth)
# print(one.vm.disksaveas(10, 0, "saved_disk", "OS", -1))

API_URI = "http://bufn1.brest.local:2633/RPC2"
one = One(pyone.OneServer(API_URI, brestadm_auth))

vm_id = 76
disks_snapshots     = {disk_snapshots_info.DISK_ID : {snapshot_info.ID: snapshot_info.NAME for snapshot_info in disk_snapshots_info.SNAPSHOT}
                            for disk_snapshots_info in one.vm.info(vm_id).SNAPSHOTS}


print(disks_snapshots)