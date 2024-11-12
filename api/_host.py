from api.one        import OneServer
from pyone.bindings import HOSTSub




class OneHost:
    def __init__(self, one_api: OneServer) -> None:
        self._one_host = one_api.host
    

    def allocate(self, hostname: str, im_mad: str = "kvm", vm_mad: str = "kvm", cluster_id: int = -1) -> int:
        return self._one_host.allocate(hostname, im_mad, vm_mad, cluster_id)
    

    def delete(self, host_id: int) -> int:
        return self._one_host.delete(host_id)
    

    def status(self, host_id: int, status_id: int) -> int:
        return self._one_host.status(host_id, status_id)
    
    def enable(self, host_id: int) -> int:
        return self.status(host_id, 0)
    
    def disable(self, host_id: int) -> int:
        return self.status(host_id, 1)
    
    def offline(self, host_id: int) -> int:
        return self.status(host_id, 2)
    

    def update(self, host_id: int, template: str, replace: bool = False) -> int:
        return self._one_host.update(host_id, template, 0 if replace else 1)
    

    def rename(self, host_id: int, new_name: str) -> int:
        return self._one_host.rename(host_id, new_name)
    

    def info(self, host_id: int, decrypt_secrets: bool = False) -> HOSTSub:
        return self._one_host.info(host_id, decrypt_secrets)
    

    def monitoring(self, host_id: int) -> str:
        return self._one_host.monitoring(host_id)
    

    