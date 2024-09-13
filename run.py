import sys
sys.path.append("api")
sys.path.append("data")
sys.path.append("utils")
sys.path.append("commands")
sys.path.append("tests")


from api    import OneSystemVersion, OneSystemConfig, ApiConnection
from utils  import print_method_fail, print_method_pass, create_oneadmin_token



SERVER      = "http://10.0.70.21:2633/RPC2"
SESSION     = create_oneadmin_token()


api_session = ApiConnection(SERVER, SESSION)






for _ in range(1):

    version     = OneSystemVersion(api_session)
    try:
        v = version.get_version()
        print(v)
    except Exception as e:
        print_method_fail(version.method_info.xml_rpc_method_name)
        print("Failure:", e)
        print(f"CLI: {version.method_info.cli_command}")
    else:
        print_method_pass(version.method_info.xml_rpc_method_name)

