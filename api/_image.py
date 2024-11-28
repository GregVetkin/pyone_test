from api.one        import OneServer
from pyone.bindings import IMAGESub



class OneImage:
    def __init__(self, one_api: OneServer) -> None:
        self._one_image = one_api.image
    
    def allocate(self, template: str, storage_id: int, check_storage_capacity: bool = True) -> int:
        """Allocates a new image in OpenNebula"""
        return self._one_image.allocate(template, storage_id, check_storage_capacity)
    
    def chmod(self, image_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1) -> int:
        """Changes the permission bits of an image"""
        
        return self._one_image.chmod(image_id, 
                                     user_use, user_manage, user_admin,
                                     group_use, group_manage, group_admin,
                                     other_use, other_manage, other_admin)
    
    def chown(self, image_id: int, user_id: int = -1, group_id: int = -1) -> int:
        """Changes the ownership of an image"""
        return self._one_image.chown(image_id, user_id, group_id)
    
    def chtype(self, image_id: int, new_type: str) -> int:
        """Changes the type of an Image"""
        return self._one_image.chtype(image_id, new_type)
    
    def clone(self, image_id: int, clone_name: str, datastore_id: int = -1) -> int:
        """Clones an existing image"""
        return self._one_image.clone(image_id, clone_name, datastore_id)
    
    def delete(self, image_id: int, force: bool = False) -> int:
        """Deletes the given image from the pool"""
        return self._one_image.delete(image_id, force)
    
    def enable(self, image_id: int, enable: bool) -> int:
        """Enables or disables an image"""
        return self._one_image.enable(image_id, enable)

    def _enable(self, image_id: int) -> int:
        """Enables an image"""
        return self.enable(image_id, True)
    
    def _disable(self, image_id: int) -> int:
        """Disables an image"""
        return self.enable(image_id, False)
    
    def persistent(self, image_id: int, persistent: bool) -> int:
        """Sets the Image as persistent or not persistent"""
        return self._one_image.persistent(image_id, persistent)

    def _persistent(self, image_id: int) -> int:
        """Sets the Image as persistent"""
        return self.persistent(image_id, True)
    
    def _nonpersistent(self, image_id: int) -> int:
        """Sets the Image as not persistent"""
        return self.persistent(image_id, False)
    
    def info(self, image_id: int, decrypt_secrets: bool = False) -> IMAGESub:
        """Retrieves information for the image"""
        return self._one_image.info(image_id, decrypt_secrets)
    
    def lock(self, image_id: int, lock_level: int = 1, check_already_locked: bool = False) -> int:
        """Locks an Image. Lock certain actions depending on blocking level"""
        return self._one_image.lock(image_id, lock_level, check_already_locked)

    def unlock(self, image_id: int) -> int:
        """Unlocks an Image"""
        return self._one_image.unlock(image_id)

    def rename(self, image_id: int, new_name: str) -> int:
        """Renames an image"""
        return self._one_image.rename(image_id, new_name)
    
    def snapshotdelete(self, image_id: int, snapshot_id: int) -> int:
        """Deletes a snapshot from the image"""
        return self._one_image.snapshotdelete(image_id, snapshot_id)

    def snapshotrevert(self, image_id: int, snapshot_id: int) -> int:
        """Reverts image state to a previous snapshot"""
        return self._one_image.snapshotrevert(image_id, snapshot_id)

    def snapshotflatten(self, image_id: int, snapshot_id: int) -> int:
        """Flatten the snapshot of image and discards others"""
        return self._one_image.snapshotflatten(image_id, snapshot_id)

    def restore(self, image_id: int, datastore_id: int, vm_name: str = "") -> int:
        """Restores a VM backup"""
        return self._one_image.restore(image_id, datastore_id, vm_name)

    def update(self, image_id: int, template: str, replace: bool = False) -> int:
        """Replaces the image template contents"""
        return self._one_image.update(image_id, template, 0 if replace else 1)
