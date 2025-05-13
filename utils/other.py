import time
from typing import Callable, Optional



def get_unic_name(
        prefix:     str = "api_test_", 
        postfix:    str = ""
    ):
    return f"{prefix}{time.time_ns()}{postfix}"



def wait_until(
        condition:          Callable[[], bool],
        timeout:            float = 60.0,
        interval:           float = 1.0,
        timeout_message:    Optional[str] = ""
    ):
    
    start = time.time()
    
    while True:
        if condition():
            return

        if time.time() - start > timeout:
            raise TimeoutError(timeout_message)

        time.sleep(interval)