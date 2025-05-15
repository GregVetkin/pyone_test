from pyone                  import OneServer
from api._system            import OneSystem
from api._image             import OneImage
from api._imagepool         import OneImagepool
from api._datastore         import OneDatastore
from api._datastorepool     import OneDatastorepool
from api._host              import OneHost
from api._hostpool          import OneHostpool
from api._template          import OneTemplate
from api._templatepool      import OneTemplatepool
from api._zone              import OneZone
from api._zonepool          import OneZonepool
from api._cluster           import OneCluster
from api._clusterpool       import OneClusterpool
from api._group             import OneGroup
from api._grouppool         import OneGrouppool
from api._groupquota        import OneGroupquota
from api._user              import OneUser
from api._userpool          import OneUserpool
from api._userquota         import OneUserquota
from api._vm                import OneVm
from api._vmpool            import OneVmpool


from time import sleep

class WaitWrapper(OneServer):
    def __init__(self, uri, session, timeout=None, https_verify=True, **options):
        super().__init__(uri, session, timeout, https_verify, **options)

    def _ServerProxy__request(self, *args, **kwargs):
        result= super()._ServerProxy__request(*args, **kwargs)
        sleep(1)
        return result



class One:
    def __init__(self, one_server: OneServer) -> None:
        self._one_api       = one_server

        self.system         = OneSystem(self._one_api)

        self.image          = OneImage(self._one_api)
        self.imagepool      = OneImagepool(self._one_api)

        self.datastore      = OneDatastore(self._one_api)
        self.datastorepool  = OneDatastorepool(self._one_api)

        self.host           = OneHost(self._one_api)
        self.hostpool       = OneHostpool(self._one_api)

        self.template       = OneTemplate(self._one_api)
        self.templatepool   = OneTemplatepool(self._one_api)

        self.zone           = OneZone(self._one_api)
        self.zonepool       = OneZonepool(self._one_api)

        self.cluster        = OneCluster(self._one_api)
        self.clusterpool    = OneClusterpool(self._one_api)

        self.group          = OneGroup(self._one_api)
        self.grouppool      = OneGrouppool(self._one_api)
        self.groupquota     = OneGroupquota(self._one_api)

        self.user           = OneUser(self._one_api)
        self.userpool       = OneUserpool(self._one_api)
        self.userquota      = OneUserquota(self._one_api)

        self.vm             = OneVm(self._one_api)
        self.vmpool         = OneVmpool(self._one_api)
        
        