from utils.connection       import SshConnectionData, ApiConnectionData, brest_admin_ssh_conn
from utils.commands         import run_command_via_ssh
from config.base            import API_URI




def get_user_name_by_id(user_id: int) -> str:
    command = f"oneuser show {user_id} --xml" + r" | grep -oP '<NAME>\K.*?(?=</NAME>)'"
    return run_command_via_ssh(brest_admin_ssh_conn, command)


def get_user_token_by_id(user_id: int) -> str:
    command = f"oneuser show {user_id} --xml" + r" | grep -oPm1 '<TOKEN>\K.*?(?=</TOKEN>)'"
    return run_command_via_ssh(brest_admin_ssh_conn, command)


def get_api_connection_by_user_id(user_id: int) -> ApiConnectionData:
    name    = get_user_name_by_id(user_id)
    token   = get_user_token_by_id(user_id)
    return ApiConnectionData(name, token, API_URI)



def kerberos_kinit(ssh_connection_data: SshConnectionData):
    kinit_command = f"echo '{ssh_connection_data.password}' | kinit"
    run_command_via_ssh(ssh_connection_data, kinit_command)

