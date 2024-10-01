class Link:
    def __init__(self, name: str, url: str):
        self.name: str = name
        self.url: str = url

    def __str__(self):
        return f"Link: {self.name}: {self.url}"
