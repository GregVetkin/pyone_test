from api.one        import OneServer
from pyone.bindings import ZONESub, RAFTSub



class OneZone:
    def __init__(self, one_api: OneServer) -> None:
        self._one_zone = one_api.zone

    def allocate(self, template: str) -> int:
        """Allocates a new zone in OpenNebula"""
        return self._one_zone.allocate(template)

    def delete(self, zone_id: int) -> int:
        """Deletes the given zone from the pool"""
        return self._one_zone.delete(zone_id)

    def enable(self, zone_id: int, enable: bool) -> int:
        "Enable/disable the given zone"
        return self._one_zone.enable(zone_id, enable)
    
    def _enable(self, zone_id: int) -> int:
        "Enables the given zone"
        return self.enable(zone_id, True)
    
    def _disable(self, zone_id: int) -> int:
        "Disables the given zone"
        return self.enable(zone_id, False)
    
    def update(self, zone_id: int, template: str, replace: bool = False) -> int:
        """Replaces the zone template contents"""
        return self._one_zone.update(zone_id, template, 0 if replace else 1)
    
    def rename(self, zone_id: int, new_name: str) -> int:
        """Renames a zone"""
        return self._one_zone.rename(zone_id, new_name)
    
    def info(self, zone_id: int, decrypt_secrets: bool = False) -> ZONESub:
        """Retrieves information for the zone"""
        return self._one_zone.info(zone_id, decrypt_secrets)

    def raftstatus(self) -> RAFTSub:
        """Retrieves raft status one servers"""
        return self._one_zone.raftstatus()

    def addserver(self, zone_id: int, template: str) -> int:
        """Add server to zone"""
        return self._one_zone.addserver(zone_id, template)

    def delserver(self, zone_id: int, server_id: int) -> int:
        """Delete a server from zone"""
        return self._one_zone.delserver(zone_id, server_id)

    def resetserver(self, zone_id: int, server_id: int) -> int:
        """Reset follower log index. This should be trigger when a follower DB has been reset"""
        return self._one_zone.resetserver(zone_id, server_id)
