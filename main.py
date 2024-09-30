import requests
from config import getConfig

class AspectaParser:
    def __init__(self, cfg: dict):
        self.cfg = cfg

    def start(self):
        print(self.cfg)


def main():
    cfg = getConfig()

    aspectaParser = AspectaParser(cfg=cfg)

    aspectaParser.start()


if __name__ == "__main__":
    main()
