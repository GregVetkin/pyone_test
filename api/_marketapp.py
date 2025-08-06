from api.one        import OneServer
from pyone.bindings import MARKETPLACEAPPSub



class OneMarketapp:
    def __init__(self, one_api: OneServer) -> None:
        self._one_marketapp = one_api.marketapp
    
    def allocate(self, template: str, market_id: int) -> int:
        """Allocates a new marketplace app in OpenNebula"""
        return self._one_marketapp.allocate(template, market_id)

    def delete(self, marketapp_id: int) -> int:
        """Deletes the given marketplace app from the pool"""
        return self._one_marketapp.delete(marketapp_id)

    def enable(self, marketapp_id: int, enable: bool) -> int:
        """Enables or disables a marketplace app"""
        return self._one_marketapp.enable(marketapp_id, enable)
    
    def update(self, marketapp_id: int, template: str, update_type: int) -> int:
        """Replaces the marketplace app template contents"""
        return self._one_marketapp.update(marketapp_id, template, update_type)
    
    def chmod(self, marketapp_id: int, 
              user_use: int, user_manage: int, user_admin: int,
              group_use: int, group_manage: int, group_admin: int,
              other_use: int, other_manage: int, other_admin: int) -> int:
        """Changes the permission bits of a marketplace app"""
        
        return self._one_marketapp.chmod(marketapp_id,
                                         user_use, user_manage, user_admin,
                                         group_use, group_manage, group_admin,
                                         other_use, other_manage, other_admin)
    
    def chown(self, marketapp_id: int, user_id: int, group_id: int) -> int:
        """Changes the ownership of a marketplace app"""
        return self._one_marketapp.chown(marketapp_id, user_id, group_id)
    
    def rename(self, marketapp_id: int, new_name: str) -> int:
        """Renames a marketplace app"""
        return self._one_marketapp.rename(marketapp_id, new_name)
    
    def info(self, marketapp_id: int, decrypt_secrets: bool = False) -> MARKETPLACEAPPSub:
        """Retrieves information for the marketplace app"""
        return self._one_marketapp.info(marketapp_id, decrypt_secrets)
    
    def lock(self, marketapp_id: int, lock_level: int, check_already_locked: bool) -> int:
        """Locks a MarketPlaceApp. Lock certain actions depending on blocking level"""
        return self._one_marketapp.lock(marketapp_id, lock_level, check_already_locked)

    def unlock(self, marketapp_id: int) -> int:
        """Unlocks a MarketPlaceApp"""
        return self._one_marketapp.unlock(marketapp_id)
    
    def export(self, marketapp_id: int, datastore_id: int):
        """https://jira.astralinux.ru/browse/BREST-4544"""
        return self._one_marketapp.export(marketapp_id, datastore_id)