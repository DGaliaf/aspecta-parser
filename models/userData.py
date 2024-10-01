import re

from models import Link, Label


class UserData:
    def __init__(self, links: list[Link], wallet: str, labels: list[Label]):
        self.name = ""
        self.links: list[Link] = links
        self.wallet: str = wallet
        self.labels: list[Label] = labels

    def __str__(self):
        labels = ""
        for label in self.labels:
            labels += f"    -{label}\n"

        links = ""
        for link in self.links:
            links += f"    -{link}\n"

        return f"----------------------\n\nUser:\n -Name: {self.name}\n -Wallet: {self.wallet}\n -Labels:\n  {labels}\n -Links:\n  {links}\n----------------------\n\n"

    def isEligible(self) -> bool:
        def __hasNeededLabel() -> bool:
            for label in self.labels:
                if re.search(
                        'dev|developer|Developer|Dev|Solidity|Engineer|engineer|solidity|backend|Backend|Frontend|frontend|manager|moderator|mod|content|Content|Manager|Programmer|programmer|intern|Intern|Collab|collab|Java|java|Go|go|Golang|golang|Flutter|flutter|Python|python|contract|Contract|Freelance|freelance|React|react',
                        label.name):
                    return True

            return False

        def __hasLink() -> bool:
            for link in self.links:
                if link.url != "" or link.url != " " or link.url is not None:
                    return True

            return False

        def __hasWallet() -> bool:
            return len(self.wallet) > 1

        if __hasNeededLabel() and __hasLink() and __hasWallet():
            return True

        return False
