import json


def open_json_file(path: str):
    with open(path) as f:
        return json.load(f)


def read_from_json_file(path: str, key: str, default: str = None):
    content_dict: dict = open_json_file(path=path)
    if key in content_dict:
        return content_dict[key]
    else:
        return default or key
