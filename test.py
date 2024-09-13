from api    import OneSystemConfig, OneSystemVersion, ApiConnection
from utils  import print_method_fail, print_method_pass




SERVER      = "http://10.0.70.21:2633/RPC2"
SESSION     = "test"


api_session = ApiConnection(SERVER, SESSION)





method_list = [OneSystemConfig, OneSystemVersion]



for method_class in method_list:
    method = method_class(api_session)
    
    try:
        

    except Exception as e:
        print_method_fail(method.method_info.xml_rpc_method_name)
        print("Failure:", e)
        print(f"CLI: {method.method_info.cli_command}")
    else:
        print_method_pass(method.method_info.xml_rpc_method_name)

