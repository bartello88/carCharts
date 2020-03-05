import yaml
from utils.tupperware import tupperware


def load(file):
    with open(file, 'r') as f:
        return tupperware(yaml.load(f, Loader=yaml.SafeLoader))


def load_string(str):
    return tupperware(yaml.load(str, Loader=yaml.SafeLoader))


def load_dict(dict):
    return tupperware(dict)
