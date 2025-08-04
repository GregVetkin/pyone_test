from api.one        import OneServer
from pyone.bindings import DEFAULT_GROUP_QUOTASTypeSub


class OneGroupquota:
    def __init__(self, one_api: OneServer) -> None:
        self._one_groupquota = one_api.groupquota

    def info(self) -> DEFAULT_GROUP_QUOTASTypeSub:
        """Returns the default group quota limits"""
        return self._one_groupquota.info()
    
    def update(self, template: str) -> DEFAULT_GROUP_QUOTASTypeSub:
        """Updates the default group quota limits"""
        return self._one_groupquota.update(template)
    
