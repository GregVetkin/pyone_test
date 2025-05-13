from api.one        import OneServer




class OneVn:
    def __init__(self, one_api: OneServer) -> None:
        self._one_vn = one_api.vn

    def allocate(self, template: str, cluster_id: int = -1) -> int:
        """Allocates a new virtual network in OpenNebula"""
        return self._one_vn.allocate(template, cluster_id)
    
    def delete(self, vn_id: int) -> int:
        """Deletes the given virtual network from the pool"""
        return self._one_vn.delete(vn_id)
