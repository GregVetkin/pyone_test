from api.one        import OneServer
from pyone.bindings import MARKETPLACESub



class OneMarket:
    def __init__(self, one_api: OneServer) -> None:
        self._one_market = one_api.market
    
    def allocate(self, template: str) -> int:
        """Allocates a new marketplace in OpenNebula"""
        return self._one_market.allocate(template)
    
    def delete(self, market_id: int) -> int:
        """Deletes the given marketplace from the pool"""
        return self._one_market.delete(market_id)

    def update(self, market_id: int, template: str, update_type: int) -> int:
        """Replaces the marketplace template contents"""
        return self._one_market.update(market_id, template, update_type)

    def chmod(self, market_id: int, 
              user_use: int, user_manage: int, user_admin: int,
              group_use: int, group_manage: int, group_admin: int,
              other_use: int, other_manage: int, other_admin: int) -> int:
        """Changes the permission bits of a marketplace"""
        
        return self._one_market.chmod(market_id,
                                      user_use, user_manage, user_admin,
                                      group_use, group_manage, group_admin,
                                      other_use, other_manage, other_admin)
    
    def chown(self, market_id: int, user_id: int, group_id: int) -> int:
        """Changes the ownership of a marketplace"""
        return self._one_market.chown(market_id, user_id, group_id)

    def rename(self, market_id: int, new_name: str) -> int:
        """Renames a marketplace"""
        return self._one_market.rename(market_id, new_name)

    def enable(self, market_id: int, enable: bool) -> int:
        """Enable/disable the Marketplace"""
        return self._one_market.enable(market_id, enable)
    
    def info(self, market_id: int, decrypt_secrets: bool = False) -> MARKETPLACESub:
        """Retrieves information for the marketplace"""
        return self._one_market.info(market_id, decrypt_secrets)
