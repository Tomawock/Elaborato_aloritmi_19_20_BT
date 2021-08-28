class Link:
    def __init__(self, name, event):
        self.name = name
        self.event = event

    def __str__(self):
        return self.name + " " + self.event

    def swap(self, new_link):
        self.name = new_link.name
        self.event = new_link.event
