import json

def load_settings(filePath):
    with open(filePath, 'r') as f:
        return json.load(f)