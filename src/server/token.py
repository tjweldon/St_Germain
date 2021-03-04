import json
import os

repl = False


def replOrLocal(environment):
    if environment is True:
        TOKEN = os.getenv("API_KEY")
        return TOKEN

    else:
        with open("data/stGermain.json", "r") as configjsonFile:
            configData = json.load(configjsonFile)
            TOKEN = configData["API_KEY"]
            return TOKEN
