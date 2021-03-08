import json
import os

repl = True
devFlag = False


def replOrLocal(environment, development):
    if environment is True and development is False:
        TOKEN = os.getenv("API_KEY")
        return TOKEN

    elif environment is False and development is True:
        with open("data/stGermain.json", "r") as configjsonFile:
            configData = json.load(configjsonFile)
            TOKEN = configData["DEV_KEY"]
            return TOKEN

    else:
        with open("data/stGermain.json", "r") as configjsonFile:
            configData = json.load(configjsonFile)
            TOKEN = configData["API_KEY"]
            return TOKEN
