import os
import json

def getConfig():
    with open('config.json') as f:
        config = json.load(f)
        return(config)
