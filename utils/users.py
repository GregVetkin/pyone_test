from utils.connection_data  import ConnectionData
from utils.commands         import run_command_via_ssh
from config.base            import LocalAdmin, BrestAdmin, API_URI, RAFT_NODE_ADDRESS, SOLO_NODE_ADDRESS




def admin_api_connection_data() -> ConnectionData:
    return ConnectionData(
        user        = BrestAdmin.USERNAME, 
        password    = get_brest_user_token(BrestAdmin.USERNAME), 
        address     = API_URI
    )




def get_brest_user_token(username: str) -> str:
    conn_data = ConnectionData(
        user     = LocalAdmin.USERNAME,
        password = LocalAdmin.PASSWORD,
        address  = SOLO_NODE_ADDRESS
    )
    command = f"sudo cat /var/lib/one/homes/{username}/one_auth"
    result  = run_command_via_ssh(conn_data, command)
    token   = result.split(":")[1]
    return token



def kerberos_kinit(ssh_connection_data: ConnectionData):
    kinit_command = f"echo '{ssh_connection_data.password}' | kinit"
    run_command_via_ssh(ssh_connection_data, kinit_command)

