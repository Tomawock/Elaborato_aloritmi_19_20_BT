from model.link import Link
from model.fa import FA


class BehavioralState:
    def __init__(self, name, list_fa_state, list_link):
        self.name = name
        self.list_fa_state = list_fa_state
        self.list_link = list_link

    def __str__(self):
        string_out = "(" + self.name + "STATI: "
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + "|"
        string_out += " EVENTI: "
        for link in self.list_link:
            string_out += link.event + "|"

        return string_out + ")"
