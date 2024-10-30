from api.one        import OneServer
from pyone.bindings import IMAGESub


class OneImage:
    def __init__(self, one_api: OneServer) -> None:
        self._one_image = one_api.image
    
    def allocate(self, template: str, storage_id: int, check_storage_capacity: bool = True) -> int:
        return self._one_image.allocate(template, storage_id, check_storage_capacity)
    

    def chmod(self, image_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1) -> int:
        
        return self._one_image.chmod(image_id, 
                                     user_use, user_manage, user_admin,
                                     group_use, group_manage, group_admin,
                                     other_use, other_manage, other_admin)
    

    def chown(self, image_id: int, user_id: int = -1, group_id: int = -1) -> int:
        return self._one_image.chown(image_id, user_id, group_id)
    

    def chtype(self, image_id: int, new_type: str) -> int:
        return self._one_image.chtype(image_id, new_type)
    
    
    def clone(self, image_id: int, clone_name: str, datastore_id: int = -1) -> int:
        return self._one_image.clone(image_id, clone_name, datastore_id)
    

    def delete(self, image_id: int, force: bool = False) -> int:
        return self._one_image.delete(image_id, force)
    

    def enable(self, image_id: int) -> int:
        return self._one_image.enable(image_id, True)
    

    def disable(self, image_id: int) -> int:
        return self._one_image.enable(image_id, False)
    

    def make_persistent(self, image_id: int) -> int:
        return self._one_image.persistent(image_id, True)
    

    def make_nonpersistent(self, image_id: int) -> int:
        return self._one_image.persistent(image_id, False)
    
    
    def info(self, image_id: int, decrypt_secrets: bool = False) -> IMAGESub:
        return self._one_image.info(image_id, decrypt_secrets)
    

    def lock(self, image_id: int, lock_level: int = 4, check_already_locked: bool = False) -> int:
        return self._one_image.lock(image_id, lock_level, check_already_locked)


    def unlock(self, image_id: int) -> int:
        return self._one_image.unlock(image_id)


    def rename(self, image_id: int, new_name: str) -> int:
        return self._one_image.rename(image_id, new_name)
    

    