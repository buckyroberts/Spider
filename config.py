import json

# Load in a config file
def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)
