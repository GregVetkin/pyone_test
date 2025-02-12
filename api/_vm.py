from api.one        import OneServer
from pyone.bindings import VMSub, MONITORING_DATASub



class OneVm:
    def __init__(self, one_api: OneServer) -> None:
        self._one_vm = one_api.vm

    def allocate(self, tempalte: str, hold_vm: bool = False) -> int:
        """Allocates a new virtual machine in OpenNebula"""
        return self._one_vm.allocate(tempalte, hold_vm)
    
    def deploy(self, vm_id: int, host_id: int, host_capacity_check: bool = True, datastore_id: int = -1, network_scheduling_template: str = "") -> int:
        """Initiates the instance of the given vmid on the target host"""
        return self._one_vm.deploy(vm_id, host_id, host_capacity_check, datastore_id, network_scheduling_template)

    def action(self, action_name: str, vm_id: int) -> int:
        """Submits an action to be performed on a virtual machine"""
        return self._one_vm.action(action_name, vm_id)
    
    def migrate(self, vm_id: int, host_id: int, live_migration: bool = False, host_capacity_check: bool = True, datastore_id: int = -1, migration_type: int = 0) -> int:
        """Migrates one virtual machine to the target host"""
        return self._one_vm.migrate(vm_id, host_id, live_migration, host_capacity_check, datastore_id, migration_type)
    
    def disksaveas(self, vm_id: int, disk_id: int, name: str, image_type: str = "", snapshot_id: int = -1) -> int:
        """Sets the disk to be saved in the given image"""
        return self._one_vm.disksaveas(vm_id, disk_id, name, image_type, snapshot_id)
    
    def disksnapshotcreate(self, vm_id: int, disk_id: int, snapshot_description: str) -> int:
        """Takes a new snapshot of the disk image"""
        return self._one_vm.disksnapshotcreate(vm_id, disk_id, snapshot_description)
    
    def disksnapshotdelete(self, vm_id: int, disk_id: int, snapshot_id: int) -> int:
        """Deletes a disk snapshot"""
        return self._one_vm.disksnapshotdelete(vm_id, disk_id, snapshot_id)
    
    def disksnapshotrevert(self, vm_id: int, disk_id: int, snapshot_id: int) -> int:
        """Reverts disk state to a previously taken snapshot"""
        return self._one_vm.disksnapshotrevert(vm_id, disk_id, snapshot_id)
    
    def disksnapshotrename(self, vm_id: int, disk_id: int, snapshot_id: int, new_name: str) -> int:
        """Renames a disk snapshot"""
        return self._one_vm.disksnapshotrename(vm_id, disk_id, snapshot_id, new_name)
    
    def attach(self, vm_id: int, disk_vector_attribute: str) -> int:
        """Attaches a new disk to the virtual machine"""
        return self._one_vm.attach(vm_id, disk_vector_attribute)
    
    def detach(self, vm_id: int, disk_id: int) -> int:
        """Detaches a disk from a virtual machine"""
        return self._one_vm.detach(vm_id, disk_id)
    
    def diskresize(self, vm_id: int, disk_id: int, new_size_str: str) -> int:
        """Resizes a disk of a virtual machine"""
        return self._one_vm.diskresize(vm_id, disk_id, new_size_str)
    
    def attachnic(self, vm_id: int, nic_vector_attribute: str) -> int:
        """Attaches a new network interface to the virtual machine"""
        return self._one_vm.attachnic(vm_id, nic_vector_attribute)
    
    def detachnic(self, vm_id: int, nic_id: int) -> int:
        """Detaches a network interface from a virtual machine"""
        return self._one_vm.detachnic(vm_id, nic_id)
    
    def chmod(self, vm_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1) -> int:
        """Changes the permission bits of a virtual machine"""
        
        return self._one_vm.chmod(vm_id, 
                                  user_use, user_manage, user_admin,
                                  group_use, group_manage, group_admin,
                                  other_use, other_manage, other_admin)
    
    def chown(self, vm_id: int, user_id: int = -1, group_id: int = -1) -> int:
        """Changes the ownership of a virtual machine"""
        return self._one_vm.chown(vm_id, user_id, group_id)
    
    def rename(self, vm_id: int, new_name: str) -> int:
        """Renames a virtual machine"""
        return self._one_vm.rename(vm_id, new_name)
    
    def snapshotcreate(self, vm_id: int, snapshot_name: str = "") -> int:
        """Creates a new virtual machine snapshot"""
        return self._one_vm.snapshotcreate(vm_id, snapshot_name)
    
    def snapshotrevert(self, vm_id: int, snapshot_id: int) -> int:
        """Reverts a virtual machine to a snapshot"""
        return self._one_vm.snapshotrevert(vm_id, snapshot_id)
    
    def snapshotdelete(self, vm_id: int, snapshot_id: int) -> int:
        """Deletes a virtual machine snapshot"""
        return self._one_vm.snapshotdelete(vm_id, snapshot_id)
    
    def resize(self, vm_id: int, template: str, host_capacity_check: bool = True) -> int:
        """Changes the capacity of the virtual machine"""
        return self._one_vm.resize(vm_id, template, host_capacity_check)

    def update(self, vm_id: int, template: str, replace: bool = False) -> int:
        """Replaces the user template contents"""
        return self._one_vm.update(vm_id, template, 0 if replace else 1)

    def updateconf(self, vm_id: int, template: str) -> int:
        """Updates (appends) a set of supported configuration attributes in the VM template"""
        return self._one_vm.updateconf(vm_id, template)
    
    def recover(self, vm_id: int, recover_operation: int) -> int:
        """Recovers a stuck VM that is waiting for a driver operation. The recovery may be done by failing or succeeding the pending operation."""
        return self._one_vm.recover(vm_id, recover_operation)
    
    def info(self, vm_id: int, decrypt_secrets: bool = False) -> VMSub:
        """Retrieves information for the virtual machine"""
        return self._one_vm.info(vm_id, decrypt_secrets)

    def monitoring(self, vm_id: int) -> MONITORING_DATASub:
        """Returns the virtual machine monitoring records"""
        return self._one_vm.monitoring(vm_id)
    
    def lock(self, vm_id: int, lock_level: int = 1, check_already_locked: bool = False) -> int:
        """Locks a Virtual Machine. Lock certain actions depending on blocking level"""
        return self._one_vm.lock(vm_id, lock_level, check_already_locked)
    
    def unlock(self, vm_id: int) -> int:
        """Unlocks a Virtual Machine"""
        return self._one_vm.unlock(vm_id)
    
    # def backup(self, vm_id: int, datastore_id: int, name: str) -> int:
    #     """Creates a new backup image for the VM"""
    #     return self._one_vm.backup(vm_id, datastore_id, name)
    
    # def attachsg(self, vm_id: int, nic_id: int, sg_id: int) -> int:
    #     """Attaches a security group to a network interface of a VM, if the VM is running it updates the associated rules"""
    #     return self._one_vm.attachsg(vm_id, nic_id, sg_id)
    
    # def detachsg(self, sg_id: int, nic_id: int) -> int:
    #     """Detaches a security group from a network interface of a VM, if the VM is running it removes the associated rules"""
    #     return self._one_vm.detachsg(sg_id, nic_id)

    