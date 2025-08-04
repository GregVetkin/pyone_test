import base64
from dataclasses    import dataclass
from config.base    import ASTRA_VERSION, DOMAIN_NAME, BREST_VERSION, LocalAdmin, BrestAdmin, API_URI, RAFT_ENABLED, RAFT_NODE_ADDRESS, SOLO_NODE_ADDRESS
from utils.version  import Version



@dataclass
class SshConnectionData:
    user:       str
    password:   str
    host:       str

    def __post_init__(self):
        if self.user != LocalAdmin.USERNAME and Version(ASTRA_VERSION) >= Version("1.8"):
            self.user += f"@{DOMAIN_NAME}"




@dataclass
class ApiConnectionData:
    user:   str
    token:  str
    uri:    str = API_URI

    def __post_init__(self):
        self.session = f"{self.user}:{self.token}"

    #     if Version(BREST_VERSION) >= Version("4"):
    #         self.session = base64.b64encode(self.session.encode()).decode()




local_admin_ssh_conn = SshConnectionData(
        user     = LocalAdmin.USERNAME,
        password = LocalAdmin.PASSWORD,
        host     = RAFT_NODE_ADDRESS if RAFT_ENABLED else SOLO_NODE_ADDRESS 
    )

brest_admin_ssh_conn = SshConnectionData(
        user     = BrestAdmin.USERNAME,
        password = BrestAdmin.PASSWORD,
        host     = RAFT_NODE_ADDRESS if RAFT_ENABLED else SOLO_NODE_ADDRESS 
    )