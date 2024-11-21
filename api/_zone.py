from api.one        import OneServer
from pyone.bindings import ZONESub




class OneZone:
    def __init__(self, one_api: OneServer) -> None:
        self._one_zone = one_api.zone
    

    def allocate(self, template: str) -> int:
        return self._one_zone.allocate(template)

    def delete(self, zone_id: int) -> int:
        return self._one_zone.delete(zone_id)


    def _enable(self, zone_id: int, enable: bool) -> int:
        return self._one_zone.enable(zone_id, enable)
    
    def enable(self, zone_id: int) -> int:
        return self._enable(zone_id, True)
    
    def disable(self, zone_id: int) -> int:
        return self._enable(zone_id, False)
    

    def update(self, zone_id: int, template: str, replace: bool = False) -> int:
        return self._one_zone.update(zone_id, template, 0 if replace else 1)
    
    def rename(self, zone_id: int, new_name: str) -> int:
        return self._one_zone.rename(zone_id, new_name)
    
    def info(self, zone_id: int, decrypt_secrets: bool = False) -> ZONESub:
        return self._one_zone.info(zone_id, decrypt_secrets)

    def raftstatus(self) -> str:
        return self._one_zone.raftstatus()


    def addserver(self, zone_id: int, template: str) -> int:
        return self._one_zone.addserver(zone_id, template)

    def delserver(self, zone_id: int, server_id: int) -> int:
        return self._one_zone.delserver(zone_id, server_id)

    def resetserver(self, zone_id: int, server_id: int) -> int:
        return self._one_zone.resetserver(zone_id, server_id)