from api.one        import OneServer
from pyone.bindings import GROUPSub




class OneGroup:
    def __init__(self, one_api: OneServer) -> None:
        self._one_group = one_api.group

    def allocate(self, name: str) -> int:
        """Allocates a new group in OpenNebula"""
        return self._one_group.allocate(name)
    
    def delete(self, group_id: int) -> int:
        """Deletes the given group from the pool"""
        return self._one_group.delete(group_id)
    
    def info(self, group_id: int, decrypt_secrets: bool = False) -> GROUPSub:
        """Retrieves information for the group"""
        return self._one_group.info(group_id, decrypt_secrets)

    def update(self, group_id: int, template: str, replace: bool = False) -> int:
        """Replaces the group template contents"""
        return self._one_group.update(group_id, template, 0 if replace else 1)
    
    def addadmin(self, group_id: int, user_id: int) -> int:
        """Adds a User to the Group administrators set"""
        return self._one_group.addadmin(group_id, user_id)
    
    def deladmin(self, group_id: int, user_id: int) -> int:
        """Removes a User from the Group administrators set"""
        return self._one_group.deladmin(group_id, user_id)
    
    def quota(self, group_id: int, template: str) -> int:
        """Sets the group quota limits"""
        return self._one_group.quota(group_id, template)
    
