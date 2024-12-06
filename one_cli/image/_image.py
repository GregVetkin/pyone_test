import os
from time                   import sleep
from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info_dataclass, _update, _exist, _lock, _unlock, _enable, _disable, _persistent, _nonpersistent
from dataclasses            import dataclass


FUNCTION_NAME = "oneimage"


def image_exist(image_id: int) -> bool:
    return _exist(FUNCTION_NAME, image_id)



def create_image(datastore_id: int, image_template: str, await_image_rdy: bool = True) -> int:
    template_file_path  = "/tmp/test_template_file"

    with open(template_file_path, "w") as file:
        file.write(image_template)

    image_id = int(run_command(f"sudo {FUNCTION_NAME} create -d {datastore_id} {template_file_path}" + " | awk '{print $2}'"))

    if await_image_rdy:
        wait_image_ready(image_id)

    os.remove(template_file_path)
    return image_id



def _get_image_state(image_id: int) -> int:
    return Image(image_id).info().STATE

def _wait_image_state(image_id: int, state_code: int, interval: float = 1.) -> None:
    while _get_image_state(image_id) != state_code:
        sleep(interval)

def wait_image_ready(image_id: int, interval: float = 1.) -> None:
    _wait_image_state(image_id, 1, interval)




class Image:
    def __init__(self, image_id: int) -> None:
        self._id       = image_id
        self._function = FUNCTION_NAME


    def info(self) -> dataclass:
        return _info_dataclass(self._function, self._id)

 
    def delete(self) -> None:
        _delete(self._function, self._id)


    def chown(self, user_id: int, group_id: int = -1) -> None:
        _chown(self._function, self._id, user_id, group_id)


    def chmod(self, octet: str) -> None:
        _chmod(self._function, self._id, octet)


    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)


    def lock(self, lock_level: int = 4) -> None:
        _lock(self._function, self._id, lock_level)


    def unlock(self) -> None:
        _unlock(self._function, self._id)


    def disable(self) -> None:
        _disable(self._function, self._id)


    def enable(self) -> None:
        _enable(self._function, self._id)


    def persistent(self) -> None:
        _persistent(self._function, self._id)


    def nonpersistent(self) -> None:
        _nonpersistent(self._function, self._id)
