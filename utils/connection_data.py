import base64
from dataclasses import dataclass
from config.base import ASTRA_VERSION, DOMAIN_NAME, BREST_VERSION



@dataclass
class SshConnectionData:
    user:       str
    password:   str
    host:       str

    def __post_init__(self):
        if int(ASTRA_VERSION.split(".")[1]) > 7:
            self.user += f"@{DOMAIN_NAME}"




@dataclass
class ApiConnectionData:
    user:   str
    token:  str
    uri:    str

    def __post_init__(self):
        self.session = f"{self.user}:{self.token}"

        if int(BREST_VERSION.split(".")[0]) > 3:
            self.session = base64.b64encode(self.session.encode()).decode()



