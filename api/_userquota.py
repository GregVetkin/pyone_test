from api.one        import OneServer



class OneUserquota:
    def __init__(self, one_api: OneServer) -> None:
        self._one_userquota = one_api.userquota

    def info(self) -> str:
        """Returns the default user quota limits"""
        return self._one_userquota.info()
    
    def update(self, template: str) -> str:
        """Updates the default user quota limits"""
        return self._one_userquota.update(template)
