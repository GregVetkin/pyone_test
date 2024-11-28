from api.one        import OneServer
from pyone.bindings import HOSTSub



class OneHost:
    def __init__(self, one_api: OneServer) -> None:
        self._one_host = one_api.host

    def allocate(self, hostname: str, im_mad: str = "kvm", vm_mad: str = "kvm", cluster_id: int = -1) -> int:
        """Allocates a new host in OpenNebula"""
        return self._one_host.allocate(hostname, im_mad, vm_mad, cluster_id)
    
    def delete(self, host_id: int) -> int:
        """Deletes the given host from the pool"""
        return self._one_host.delete(host_id)

    def status(self, host_id: int, status_code: int) -> int:
        """Sets the status of the host"""
        return self._one_host.status(host_id, status_code)
    
    def _enable(self, host_id: int) -> int:
        """Sets the status of the host to enable"""
        return self.status(host_id, 0)
    
    def _disable(self, host_id: int) -> int:
        """Sets the status of the host to disable"""
        return self.status(host_id, 1)
    
    def _offline(self, host_id: int) -> int:
        """Sets the status of the host to offline"""
        return self.status(host_id, 2)
    
    def update(self, host_id: int, template: str, replace: bool = False) -> int:
        """Replaces the host's template contents"""
        return self._one_host.update(host_id, template, 0 if replace else 1)

    def rename(self, host_id: int, new_name: str) -> int:
        """Renames a host"""
        return self._one_host.rename(host_id, new_name)
    
    def info(self, host_id: int, decrypt_secrets: bool = False) -> HOSTSub:
        """Retrieves information for the host"""
        return self._one_host.info(host_id, decrypt_secrets)

    def monitoring(self, host_id: int) -> str:
        """Returns the host monitoring records"""
        return self._one_host.monitoring(host_id)
