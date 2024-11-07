from api.one        import OneServer
from pyone.bindings import DATASTORESub




class OneDatastore:
    def __init__(self, one_api: OneServer) -> None:
        self._one_ds = one_api.datastore
    

    def allocate(self, datastore_template: str, cluster_id: int = -1) -> int:
        return self._one_ds.allocate(datastore_template, cluster_id)
    

    def delete(self, datastore_id: int) -> int:
        return self._one_ds.delete(datastore_id)
    

    def update(self, datastore_id: int, template: str, replace: bool = False) -> int:
        return self._one_ds.update(datastore_id, template, 0 if replace else 1)
    

    def chmod(self, datastore_id: int, 
              user_use: int = -1, user_manage: int = -1, user_admin: int = -1,
              group_use: int = -1, group_manage: int = -1, group_admin: int = -1,
              other_use: int = -1, other_manage: int = -1, other_admin: int = -1) -> int:
        
        return self._one_ds.chmod(datastore_id, 
                                    user_use, user_manage, user_admin,
                                    group_use, group_manage, group_admin,
                                    other_use, other_manage, other_admin)
    

    def chown(self, datastore_id: int, user_id: int = -1, group_id: int = -1) -> int:
        return self._one_ds.chown(datastore_id, user_id, group_id)
    

    def rename(self, datastore_id: int, new_name: str) -> int:
        return self._one_ds.rename(datastore_id, new_name)
    

    def enable(self, datastore_id: int) -> int:
        return self._one_ds.enable(datastore_id, True)
    

    def disable(self, datastore_id: int) -> int:
        return self._one_ds.enable(datastore_id, False)
    

    def info(self, datastore_id: int, decrypt_secrets: bool = False) -> DATASTORESub:
        return self._one_ds.info(datastore_id, decrypt_secrets)
    

