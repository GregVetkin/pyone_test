from api.one        import OneServer
from pyone.bindings import DATASTORESub



class OneDatastore:
    def __init__(self, one_api: OneServer) -> None:
        self._one_ds = one_api.datastore
    
    def allocate(self, datastore_template: str, cluster_id: int) -> int:
        """Allocates a new datastore in OpenNebula"""
        return self._one_ds.allocate(datastore_template, cluster_id)

    def delete(self, datastore_id: int) -> int:
        """Deletes the given datastore from the pool"""
        return self._one_ds.delete(datastore_id)
    
    def update(self, datastore_id: int, template: str, update_type: int) -> int:
        """Replaces the datastore template contents"""
        return self._one_ds.update(datastore_id, template, update_type)
    
    def chmod(self, datastore_id: int, 
              user_use: int, user_manage: int, user_admin: int,
              group_use: int, group_manage: int, group_admin: int,
              other_use: int, other_manage: int, other_admin: int) -> int:
        """Changes the permission bits of a datastore"""
        
        return self._one_ds.chmod(datastore_id, 
                                    user_use, user_manage, user_admin,
                                    group_use, group_manage, group_admin,
                                    other_use, other_manage, other_admin)
    
    def chown(self, datastore_id: int, user_id: int, group_id: int) -> int:
        """Changes the ownership of a datastore"""
        return self._one_ds.chown(datastore_id, user_id, group_id)
    
    def rename(self, datastore_id: int, new_name: str) -> int:
        """Renames a datastore"""
        return self._one_ds.rename(datastore_id, new_name)
    
    def enable(self, datastore_id: int, enable: bool) -> int:
        """Enables a datastore"""
        return self._one_ds.enable(datastore_id, enable)

    def info(self, datastore_id: int, decrypt_secrets: bool = False) -> DATASTORESub:
        """Retrieves information for the datastore"""
        return self._one_ds.info(datastore_id, decrypt_secrets)
    

