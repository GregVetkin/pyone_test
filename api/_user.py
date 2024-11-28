from api.one        import OneServer
from pyone.bindings import USERSub
from typing         import List



class OneUser:
    def __init__(self, one_api: OneServer) -> None:
        self._one_user = one_api.user

    def allocate(self, username: str, password: str, auth_driver: str = "", group_ids: List[int] = []) -> int:
        """Allocates a new user in OpenNebula"""
        return self._one_user.allocate(username, password, auth_driver, group_ids)
    
    def delete(self, user_id: int) -> int:
        """Deletes the given user from the pool"""
        return self._one_user.delete(user_id)

    def passwd(self, user_id: int, new_password: str) -> int:
        """Changes the password for the given user"""
        return self._one_user.passwd(user_id, new_password)
    
    def login(self, user_id: int, token: str = "", period: int = 0, group_id: int = -1) -> str:
        """Generates or sets a login token"""
        return self._one_user.login(user_id, token, period, group_id)
    
    def update(self, user_id: int, template: str, replace: bool = False) -> int:
        """Replaces the user template contents"""
        return self._one_user.update(user_id, template, 0 if replace else 1)
    
    def chauth(self, user_id: int, auth_driver: str, new_password: str = "") -> int:
        """Changes the authentication driver and the password for the given user"""
        return self._one_user.chauth(user_id, auth_driver, new_password)
    
    def quota(self, user_id: int, quota_template: str) -> int:
        """Sets the user quota limits"""
        return self._one_user.quota(user_id, quota_template)
    
    def chgrp(self, user_id: int, group_id: int) -> int:
        """Changes the group of the given user"""
        return self._one_user.chgrp(user_id, group_id)
    
    def addgroup(self, user_id: int, group_id: int) -> int:
        """Adds the User to a secondary group"""
        return self._one_user.addgroup(user_id, group_id)
    
    def delgroup(self, user_id: int, group_id: int) -> int:
        """Removes the User from a secondary group"""
        return self._one_user.delgroup(user_id, group_id)
    
    def enable(self, user_id: int, enable: bool) -> int:
        """Enables or disables a user"""
        return self._one_user.enable(user_id, enable)
    
    def _enable(self, user_id: int) -> int:
        """Enables a user"""
        return self.enable(user_id, True)
    
    def _disable(self, user_id: int) -> int:
        """Disables a user"""
        return self.enable(user_id, False)
    
    def info(self, user_id: int = -1, decrypt_secrets: bool = False) -> USERSub:
        """Retrieves information for the user"""
        return self._one_user.info(user_id, decrypt_secrets)
