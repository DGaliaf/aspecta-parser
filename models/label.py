class Label:
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self):
        return f"Label: {self.name}"