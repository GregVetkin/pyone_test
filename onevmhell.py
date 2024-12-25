import random

methods = [
    #(method_name, is_done, difficulty, hours_to_do)
    ("one.vm.deploy", False, 3, 3),
    ("one.vm.action", False, 3, 15),
    ("one.vm.migrate", False, 1, 3),
    ("one.vm.disksaveas", False, 1, 3),
    ("one.vm.disksnapshotcreate", False, 1, 3),
    ("one.vm.disksnapshotdelete", False, 1, 3),
    ("one.vm.disksnapshotrevert", False, 1, 3),
    ("one.vm.disksnapshotrename", False, 1, 3),
    ("one.vm.attach", True, 1, 1),
    ("one.vm.detach", True, 1, 1),
    ("one.vm.diskresize", True, 1, 1),
    ("one.vm.attachnic", True, 1, 1),
    ("one.vm.detachnic", True, 1, 1),
    ("one.vm.updatenic", False, 1, 2),
    ("one.vm.allocate", True, 1, 1),
    ("one.vm.info", False, 1, 3),
    ("one.vm.chown", True, 1, 1),
    ("one.vm.chmod", True, 1, 1),
    ("one.vm.rename", True, 1, 1),
    ("one.vm.snapshotcreate", False, 2, 3),
    ("one.vm.snapshotdelete", False, 2, 3),
    ("one.vm.snapshotrevert", False, 2, 3),
    ("one.vm.resize", True, 1, 2),
    ("one.vm.update", True, 1, 2),
    ("one.vm.recover", False, 2, 3),
    ("one.vm.updateconf", False, 2, 3),
    ("one.vmpool.info", False, 2, 4),
    ("one.vmpool.infoextended", False, 2, 5),
    ("one.vm.lock", True, 1, 1),
    ("one.vm.unlock", True, 1, 1),
    ("one.vmpool.infoset", False, 2, 3),
    ("one.vmpool.monitoring", False, 2, 4),
]


for _ in methods:
    if _[1]:
        continue
    
    if not _[1] and (_[2] == 1) and (_[3] < 3):
        print(_[0])

