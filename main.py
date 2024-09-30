import asyncio

import requests
from config import getConfig
from utils import initFolders
import utils.fileUtils as fileUtils


class Link:
    def __init__(self, name: str, url: str):
        self.name: str = name
        self.url: str = url

    def __str__(self):
        return f"{self.name}: {self.url}"


class Label:
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self):
        return f"Label: {self.name}"


class UserData:
    # TODO: Print output
    def __init__(self, links: list[Link], wallet: str, labels: list[Label]):
        self.links: list[Link] = links
        self.wallet: str = wallet
        self.labels: list[Label] = labels


class AspectaParser:
    def __init__(self, cfg: dict):
        self.cfg: dict = cfg

    @staticmethod
    def __genHeader(user: str) -> dict:
        return {
            'accept': 'application/json',
            'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': '_ga=GA1.1.2054254009.1727411566; wagmi.store={"state":{"connections":{"__type":"Map","value":[]},"chainId":1,"current":null},"version":2}; _ga_JGRSFSYHNK=GS1.1.1727699494.5.1.1727699836.0.0.0',
            'priority': 'u=1, i',
            'referer': f'https://aspecta.ai/u/{user}',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }

    def __parseUserLinks(self, user: str) -> (list[Link], str):
        url: str = f"https://aspecta.ai/api/profile/users/{user}/profile/modules/connected_links/"

        response: dict = requests.get(url, headers=self.__genHeader(user)).json()

        links: list[Link] = []
        for prof in response.get("professional"):
            links.append(Link(name=prof.get("display_provider"), url=prof.get("url")))

        for soc in response.get("social"):
            links.append(Link(name=soc.get("display_provider"), url=soc.get("url")))

        wallet: str = response.get("web3")[0].get("uid")

        return links, wallet

    def __parseUserLabels(self, user) -> list[Label]:
        url: str = f"https://aspecta.ai/api/profile/users/{user}/labels/"

        response: dict = requests.get(url, headers=self.__genHeader(user)).json()

        labels: list[Label] = []
        for label in response.get("custom_labels"):
            labels.append(Label(name=label.get("display_name")))

        return labels

    def parseUserData(self, user: str) -> UserData:
        links, wallet = self.__parseUserLinks(user)
        labels = self.__parseUserLabels(user)

        return UserData(
            wallet=wallet,
            links=links,
            labels=labels
        )

    def parseUserFriends(self, user: str):
        pass

    async def start(self):
        directory = self.cfg.get("usersDatabase").get("dirPath")
        toParseFile = self.cfg.get("usersDatabase").get("files").get("toParse")

        users: list[str] = fileUtils.readFile(directory, toParseFile)
        for user in users:
            userData: UserData = self.parseUserData(user=user)
            # self.parseUserFriends(user=user)
            print(userData)
            # TODO: Add database of "parsed users" and "to parse user"
        pass


async def main():
    cfg = getConfig()

    initFolders(cfg=cfg)

    aspectaParser = AspectaParser(cfg=cfg)
    await aspectaParser.start()


if __name__ == "__main__":
    asyncio.run(main())
