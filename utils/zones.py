import json

def load_zones(path):
    with open(path, 'r') as f:
        return json.load(f)
