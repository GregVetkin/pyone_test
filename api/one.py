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
from api._vn                import OneVn


from utils.connection  import ApiConnectionData


class One():
    def __init__(self, api_connection_data: ApiConnectionData) -> None:
        uri     = api_connection_data.uri
        session = api_connection_data.session
        self._server = OneServer(uri, session)


        self.system         = OneSystem(self._server)

        self.image          = OneImage(self._server)
        self.imagepool      = OneImagepool(self._server)

        self.datastore      = OneDatastore(self._server)
        self.datastorepool  = OneDatastorepool(self._server)

        self.host           = OneHost(self._server)
        self.hostpool       = OneHostpool(self._server)

        self.template       = OneTemplate(self._server)
        self.templatepool   = OneTemplatepool(self._server)

        self.zone           = OneZone(self._server)
        self.zonepool       = OneZonepool(self._server)

        self.cluster        = OneCluster(self._server)
        self.clusterpool    = OneClusterpool(self._server)

        self.group          = OneGroup(self._server)
        self.grouppool      = OneGrouppool(self._server)
        self.groupquota     = OneGroupquota(self._server)

        self.user           = OneUser(self._server)
        self.userpool       = OneUserpool(self._server)
        self.userquota      = OneUserquota(self._server)

        self.vm             = OneVm(self._server)
        self.vmpool         = OneVmpool(self._server)
        
        self.vn             = OneVn(self._server)