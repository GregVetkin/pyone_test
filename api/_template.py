from api.one        import OneServer
from pyone.bindings import VMTEMPLATESub




class OneTemplate:
    def __init__(self, one_api: OneServer) -> None:
        self._one_template = one_api.template


    def allocate(self, template: str) -> int:
        return self._one_template.allocate(template)
    

    def clone(self, template_id: int, clone_name: str, clone_disks: bool = False) -> int:
        return self._one_template.clone(template_id, clone_name, clone_disks)
    

    def delete(self, template_id: int, delete_images: bool = False) -> int:
        return self._one_template.delete(template_id, delete_images)


    def instantiate(self, template_id: int, vm_name: str = "", hold_vm: bool = False, extra_template: str = "", private_persistent_copy: bool = False) -> int:
        return self._one_template.instantiate(template_id, vm_name, hold_vm, extra_template, private_persistent_copy)


    def update(self, template_id: int, template: str, replace: bool = False) -> int:
        return self._one_template.update(template_id, template, 0 if replace else 1)


    def chmod(self, template_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1,
              chmod_images: bool = False) -> int:
        
        return self._one_template.chmod(template_id, 
                                        user_use, user_manage, user_admin,
                                        group_use, group_manage, group_admin,
                                        other_use, other_manage, other_admin,
                                        chmod_images)

    
    def chown(self, template_id: int, user_id: int = -1, group_id: int = -1) -> int:
        return self._one_template.chown(template_id, user_id, group_id)

    
    def rename(self, template_id: int, new_name: str) -> int:
        return self._one_template.rename(template_id, new_name)
    

    def info(self, template_id: int, extended: bool = False, decrypt_secrets: bool = False) -> VMTEMPLATESub:
        return self._one_template.info(template_id, extended, decrypt_secrets)
    

    def lock(self, template_id: int, lock_level: int = 1, check_already_locked: bool = False) -> int:
        return self._one_template.lock(template_id, lock_level, check_already_locked)


    def unlock(self, template_id: int) -> int:
        return self._one_template.unlock(template_id)
    
