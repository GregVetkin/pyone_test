from pyone                  import OneServer
from api._system            import OneSystem
from api._image             import OneImage
from api._imagepool         import OneImagepool
from api._datastore         import OneDatastore
from api._datastorepool     import OneDatastorepool
from api._host              import OneHost
from api._hostpool          import OneHostpool



class One():
    def __init__(self, one_server: OneServer) -> None:
        self._one_api   = one_server

        self.system         = OneSystem(self._one_api)

        self.image          = OneImage(self._one_api)
        self.imagepool      = OneImagepool(self._one_api)

        self.datastore      = OneDatastore(self._one_api)
        self.datastorepool  = OneDatastorepool(self._one_api)

        self.host           = OneHost(self._one_api)
        self.hostpool       = OneHostpool(self._one_api)

