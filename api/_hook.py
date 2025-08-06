from api.one        import OneServer
from pyone.bindings import HOOKSub



class OneHook:
    def __init__(self, one_api: OneServer) -> None:
        self._one_hook = one_api.hook

    def allocate(self, template: str) -> int:
        """Allocates a new Hook in OpenNebula"""
        return self._one_hook.allocate(template)
    
    def delete(self, hook_id: int) -> int:
        """Deletes the given hook from the pool"""
        return self._one_hook.delete(hook_id)
    
    def update(self, hook_id: int, template: str, update_type: int) -> int:
        """Replaces the hook contents"""
        return self._one_hook.update(hook_id, template, update_type)
    
    def rename(self, hook_id: int, new_name: str) -> int:
        """Renames a hook"""
        return self._one_hook.rename(hook_id, new_name)
    
    def info(self, hook_id: int, decrypt_secrets: bool = False) -> HOOKSub:
        """Retrieves information for the hook"""
        return self._one_hook.info(hook_id, decrypt_secrets)
    
    def lock(self, hook_id: int, lock_level: int, check_already_locked: bool) -> int:
        """Locks a hook"""
        return self._one_hook.lock(hook_id, lock_level, check_already_locked)

    def unlock(self, hook_id: int) -> int:
        """Unlocks a hook"""
        return self._one_hook.unlock(hook_id)
    
    def retry(self, hook_id: int, execution_id: int) -> int:
        """Retries a hook execution"""
        return self._one_hook.retry(hook_id, execution_id)
    