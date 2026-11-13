import os
import json

def getConfig():
    with open('config.json') as f:
        config = json.load(f)
        return(config)

def writeConfig(key, value):
    with open('config.json', "r") as f:
        config = json.load(f)
        config[key] = value
    with open('config.json', "w") as f:
        json.dump(config, f)
    return(config)