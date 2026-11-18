import os

def getConfig():
    return dict(os.environ)

def writeConfig(key, value):
    os.environ[key] = str(value)
    return dict(os.environ)

