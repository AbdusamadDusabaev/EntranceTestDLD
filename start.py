import shlex
import subprocess


def install_requirements():
    command_1_str: str = "pip install --upgrade pip"
    command_1: list[str] = shlex.split(command_1_str)
    subprocess.run(command_1, capture_output=True)
    print(f"{command_1_str}\tOK")

    command_2_str: str = "pip3 install -r requirements.txt"
    command_2: list[str] = shlex.split(command_2_str)
    subprocess.run(command_2, capture_output=True)
    print(f"{command_2_str}\tOK")


def set_up_database():
    commands = [
        "makemigrations",
        "migrate",
        "loaddata api/fixtures/users.json",
        "loaddata api/fixtures/authors.json",
        "loaddata api/fixtures/tokens.json",
        "loaddata api/fixtures/books.json"
    ]
    for sub_command in commands:
        command_str: str = f"python3 manage.py {sub_command}"
        command: list[str] = shlex.split(command_str)
        subprocess.run(command, capture_output=True)
        print(f"{command_str}\tOK")


if __name__ == '__main__':
    install_requirements()
    set_up_database()
