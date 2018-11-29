import json


def load_constants(path="constants.json"):
    with open(path, "r") as i:
        return json.load(i)
