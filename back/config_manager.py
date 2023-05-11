import json


def get_config(SCRIPT_PATH: str) -> dict:
    """parsing <SCRIPT_PATH>/misc/config.json file"""
    with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
        return json.load(f)


def set_config(SCRIPT_PATH: str, current_config: dict) -> None:
    """writing prepared dict to <SCRIPT_PATH>/misc/config.json file"""
    with open(f"{SCRIPT_PATH}/misc/config.json", "w") as f:
        f.write(json.dumps(current_config))
