from time                   import sleep
from config                 import COMMAND_EXECUTOR
from utils                  import run_command
from one_cli.image._common  import ImageInfo, parse_image_info_from_xml




def image_exist(image_id: int) -> bool:
    exec_code = int(run_command(COMMAND_EXECUTOR + " " + f"oneimage show {image_id} &>/dev/null; echo $?"))
    return True if exec_code == 0 else False



def create_image_by_tempalte(datastore_id: int, image_template: str, await_image_rdy: bool = True) -> int:
    template_file_path  = "/tmp/test_template_file"

    if "ssh" in COMMAND_EXECUTOR:
        run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {template_file_path}\n{image_template}\nEOF\'")
    else:
        run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {template_file_path}\n{image_template}\nEOF")


    image_id = int(run_command(COMMAND_EXECUTOR + " " + f"oneimage create -d {datastore_id} {template_file_path}" + " | awk '{print $2}'"))

    if await_image_rdy:
        Image(image_id).wait_ready_status()

    run_command(COMMAND_EXECUTOR + " " + f"rm -f {template_file_path}")
    return image_id






class Image:
    def __init__(self, image_id: int) -> None:
        self._id = image_id
        self._lock_levels  = {
            1: "--use",
            2: "--manage",
            3: "--admin",
            4: "--all",
        }


    def info(self) -> ImageInfo:
        return parse_image_info_from_xml(run_command(COMMAND_EXECUTOR + " " + f"oneimage show {self._id} -x"))

 
    def delete(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage delete {self._id}")


    def wait_ready_status(self, interval: float = 1.) -> None:
        while self.info().STATE != 1:
            sleep(interval)


    def chown(self, user_id: int, group_id: int = -1) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage chown {self._id} {user_id} {group_id if group_id != -1 else ''}")


    def chmod(self, mod: str) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage chmod {self._id} {mod}")


    def make_persistent(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage persistent {self._id}")


    def make_nonpersistent(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage nonpersistent {self._id}")


    def lock(self, lock_level: int = 4) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage lock {self._id} {self._lock_levels[lock_level]}")


    def unlock(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage unlock {self._id}")


    def disable(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage disable {self._id}")


    def enable(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneimage enable {self._id}")





