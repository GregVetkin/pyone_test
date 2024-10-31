import subprocess



def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"{e.stderr}")
        raise
        