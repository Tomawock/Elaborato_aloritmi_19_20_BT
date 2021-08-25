class Link:
    def __init__(self, name, event):
        self.name = name
        self.event = event

    def __str__(self):
        return self.name + " " + self.event
