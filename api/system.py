from data       import SystemConfigMethodInfo, SystemVersionMethodInfo
from api.base   import Method, ApiConnection






class OneSystemVersion(Method):
    def __init__(self, api: ApiConnection) -> None:
        super().__init__(api=api, method_info=SystemVersionMethodInfo)

    def get_version(self) -> str:
        return self._api.system.version()





class OneSystemConfig(Method):
    def __init__(self, api: ApiConnection) -> None:
        super().__init__(api=api, method_info=SystemConfigMethodInfo)

    def get_config(self) -> str:
        return self._api.system.config()
    

    