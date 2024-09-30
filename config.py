import json
import os

from dotenv import load_dotenv

load_dotenv()

__configPath: str = os.getenv("CONFIG_PATH")


def getConfig() -> dict:
    return json.load(open(__configPath, 'r'))
