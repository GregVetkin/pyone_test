import sys
sys.path.append("api")
sys.path.append("data")
sys.path.append("utils")


from api    import OneSystemVersion, OneSystemConfig, ApiConnection
from utils  import print_method_fail, print_method_pass



SERVER      = "http://10.0.70.21:2633/RPC2"
SESSION     = "oneadmin:89f2e258d42eeaa7c9e2c42d5c9f31e11f315b074d5a164a71d9c9ba7fdc8a91"
api_session = ApiConnection(SERVER, SESSION)







for _ in range(10):

    version     = OneSystemVersion(api_session)
    try:
        version.get_version()
    except Exception as e:
        print_method_fail(version.method_info.xml_rpc_method_name)
        print("Failure:", e)
        print(f"Usage with cli: {version.method_info.cli_command}")
    else:
        print_method_pass(version.method_info.xml_rpc_method_name)

