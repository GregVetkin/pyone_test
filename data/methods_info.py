from dataclasses import dataclass





@dataclass
class MethodInfo:
    cli_command:            str = "-"
    xml_rpc_method_name:    str = "-"





SystemVersionMethodInfo     = MethodInfo(cli_command="-", 
                                         xml_rpc_method_name="one.system.version")

SystemConfigMethodInfo      = MethodInfo(cli_command="-",
                                         xml_rpc_method_name="one.system.config")

