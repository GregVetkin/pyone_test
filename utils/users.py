from utils.connection       import SshConnectionData, ApiConnectionData, brest_admin_ssh_conn
from utils.commands         import run_command_via_ssh
from config.base            import LocalAdmin, SOLO_NODE_ADDRESS, RAFT_NODE_ADDRESS, RAFT_ENABLED, ASTRA_VERSION, DOMAIN_NAME, API_URI




# def get_user_token(username: str) -> str:
#     if Version(ASTRA_VERSION) > Version("1.7"):
#         username += f"@{DOMAIN_NAME}"

#     command = f"sudo cat /var/lib/one/homes/{username}/one_auth"
#     result  = run_command_via_ssh(local_admin_ssh_conn, command)
#     token   = result.split(":")[1]
#     return token



def get_api_connection_by_user_id(user_id: int) -> ApiConnectionData:
    get_user_xml        = f"oneuser show {user_id} --xml"
    get_name_command    = get_user_xml + r" | grep -oP '<NAME>\K.*?(?=</NAME>)'"
    get_token_command   = get_user_xml + r" | grep -oPm1 '<TOKEN>\K.*?(?=</TOKEN>)'"
    
    name    = run_command_via_ssh(brest_admin_ssh_conn, get_name_command)
    token   = run_command_via_ssh(brest_admin_ssh_conn, get_token_command)

    return ApiConnectionData(name, token, API_URI)



def kerberos_kinit(ssh_connection_data: SshConnectionData):
    kinit_command = f"echo '{ssh_connection_data.password}' | kinit"
    run_command_via_ssh(ssh_connection_data, kinit_command)

