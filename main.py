import asyncio

import requests
from config import getConfig
from models import Link, Label
from models.userData import UserData
from utils import initFolders
import utils.fileUtils as fileUtils


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

        if response.get("detail") == "Not found.":
            print(f"[-] {user.capitalize()} not found.")
            return [], ""

        links: list[Link] = []
        for prof in response.get("professional"):
            links.append(Link(name=prof.get("display_provider"), url=prof.get("url")))

        for soc in response.get("social"):
            links.append(Link(name=soc.get("display_provider"), url=soc.get("url")))

        if len(response.get("web3")) == 0:
            wallet = ""
        else:
            wallet: str = response.get("web3")[0].get("uid")

        return links, wallet

    def __parseUserLabels(self, user: str) -> list[Label]:
        url: str = f"https://aspecta.ai/api/profile/users/{user}/labels/"

        response: dict = requests.get(url, headers=self.__genHeader(user)).json()

        labels: list[Label] = []
        if response.get("custom_labels") is not None:
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

    def parseUserFriends(self, user: str) -> list[str]:
        url: str = f"https://aspecta.ai/api/recommendation/users/{user}/recommendation-users?source=PC"

        response: dict = requests.request("GET", url, headers=self.__genHeader(user)).json()

        friends: list[str] = []
        for comFriend in response.get("common_recommend"):
            friends.append(comFriend.get("username"))

        for valFriend in response.get("valuable_recommend"):
            friends.append(valFriend.get("username"))

        return friends

    async def start(self):
        userDirectory = self.cfg.get("usersDatabase").get("dirPath")
        outputDirectory = self.cfg.get("outputDatabase").get("dirPath")
        toParseFile = self.cfg.get("usersDatabase").get("files").get("toParse")
        parsedFile = self.cfg.get("usersDatabase").get("files").get("parsed")

        print(f"[+] Start parsing...")

        while True:
            print(f"[+] Getting users...")
            users: list[str] = fileUtils.readFile(userDirectory, toParseFile)
            print(f"[+] Total users - {len(users)}")

            for user in users:
                print(f"[+] Parsing {user.strip()}...")
                if fileUtils.isLineInFile(userDirectory, parsedFile, user.strip()):
                    print(f"[+] User - {user.strip()} already was parsed, passing him")
                    continue

                print(f"[+] Getting user data...")
                userData: UserData = self.parseUserData(user=user.strip())
                userData.name = user.capitalize()
                print(f"[+] User data:\n{userData}")
                print(f"[+] Getting user friends...")
                friends = self.parseUserFriends(user=user.strip())
                print(f"[+] Got {len(friends)} {user.strip()}`s friends")

                if userData.isEligible():
                    print(f"[+] User - {user.strip()} is eligible")
                    eligiblePath = self.cfg.get("outputDatabase").get("files").get("eligible")
                else:
                    print(f"[+] User - {user.strip()} is not eligible")
                    eligiblePath = self.cfg.get("outputDatabase").get("files").get("notEligible")

                await fileUtils.deleteLineAsync(userDirectory, toParseFile, user)
                await fileUtils.writeMultipleToFileAsync(userDirectory, toParseFile, friends)
                await fileUtils.writeToFileAsync(userDirectory, parsedFile, user)
                await fileUtils.writeToFileAsync(outputDirectory, eligiblePath, userData.__str__())

        print(f"[+] Parsing end")


async def main():
    cfg = getConfig()

    initFolders(cfg=cfg)

    aspectaParser = AspectaParser(cfg=cfg)
    await aspectaParser.start()


if __name__ == "__main__":
    asyncio.run(main())
