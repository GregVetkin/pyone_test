from api.one import OneServer

class OneImage:
    def __init__(self, one_api: OneServer) -> None:
        self._one_image = one_api.image
    
    def allocate(self, template: str, storage_id: int, check_storage_capacity: bool = True) -> int:
        return self._one_image.allocate(template, storage_id, check_storage_capacity)
    

    def chmod(self, image_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1) -> int:
        
        return self._one_image.chmod(image_id, user_use, user_manage, user_admin,
                                     group_use, group_manage, group_admin,
                                     other_use, other_manage, other_admin)
    

    def chown(self, image_id: int, user_id: int = -1, group_id: int = -1) -> int:
        return self._one_image.chown(image_id, user_id, group_id)
    

    def chtype(self, image_id: int, new_type: str) -> int:
        return self._one_image.chtype(image_id, new_type)
    
    