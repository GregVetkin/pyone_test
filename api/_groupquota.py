from api.one        import OneServer




class OneGroupquota:
    def __init__(self, one_api: OneServer) -> None:
        self._one_groupquota = one_api.groupquota

    def info(self) -> str:
        """Returns the default group quota limits"""
        return self._one_groupquota.info()
    
    def update(self, template: str) -> str:
        """Updates the default group quota limits"""
        return self._one_groupquota.update(template)
    
    