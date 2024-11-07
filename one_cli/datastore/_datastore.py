from config                     import COMMAND_EXECUTOR
from utils                      import run_command
from one_cli.datastore._common  import DatastoreInfo, parse_datastore_info_from_xml



def datastore_exist(datastore_id: int) -> bool:
    exec_code = int(run_command(COMMAND_EXECUTOR + " " + f"onedatastore show {datastore_id} &>/dev/null; echo $?"))
    return True if exec_code == 0 else False


def create_ds_by_tempalte(ds_template: str) -> int:
    template_file_path  = "/tmp/test_template_file"

    if "ssh" in COMMAND_EXECUTOR:
        run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {template_file_path}\n{ds_template}\nEOF\'")
    else:
        run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {template_file_path}\n{ds_template}\nEOF")

    ds_id = int(run_command(COMMAND_EXECUTOR + " " + f"onedatastore create {template_file_path}" + " | awk '{print $2}'"))
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {template_file_path}")

    return ds_id








class Datastore:
    def __init__(self, ds_id: int) -> None:
        self._id = ds_id
    
    def delete(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onedatastore delete {self._id}")

    def chmod(self, mod: str) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onedatastore chmod {self._id} {mod}")

    def info(self) -> DatastoreInfo:
        return parse_datastore_info_from_xml(run_command(COMMAND_EXECUTOR + " " + f"onedatastore show {self._id} -x"))
    
    def update(self, template: str, append: bool = False) -> None:
        file = "/tmp/test_file"
        if "ssh" in COMMAND_EXECUTOR:
            run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {file}\n{template}\nEOF\'")
        else:
            run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {file}\n{template}\nEOF")
        append_flag = "-a" if append else ""
        run_command(COMMAND_EXECUTOR + " " + f"onedatastore update {self._id} {file} {append_flag}")
        run_command(COMMAND_EXECUTOR + " " + f"rm -f {file}")