from dataclasses import dataclass


@dataclass
class TestData:
    xml_rpc_method:     str
    test_file_path:     str
    cli_command:        str
