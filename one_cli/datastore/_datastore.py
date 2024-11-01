from config                 import COMMAND_EXECUTOR
from utils                  import run_command





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