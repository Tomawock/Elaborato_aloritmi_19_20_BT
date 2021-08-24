from model.link import Link
from model.fa import FA


class BehavioralState:
    def __init__(self, name, list_fa_state, list_link):
        self.name = name
        self.list_fa_state = list_fa_state
        self.list_link = list_link
