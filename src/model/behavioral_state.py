from model.link import Link
from model.fa import FA


class BehavioralState:
    def __init__(self, name, list_fa_state, list_link):
        self.name = name
        self.list_fa_state = list_fa_state
        self.list_link = list_link

    def __str__(self):
        string_out = "( LABEL: " + str(self.name) + "|STATI: "
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + "|"
        string_out += " EVENTI: "
        for link in self.list_link:
            string_out += link.event + "|"

        return string_out + ")"

    def short_str(self):
        string_out = "(" + str(self.name) + "|"
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + "|"
        string_out += "|"
        for link in self.list_link:
            string_out += link.event + "|"

        return string_out + ")"

    def __eq__(self, other):
        equal = True
        if not isinstance(other, BehavioralState):
            equal = False
        for i in range(len(self.list_fa_state)):
            # [1] identifica la seconda posizione, quindi lo stato
            if self.list_fa_state[i][1].name != other.list_fa_state[i][1].name:
                equal = False
        for i in range(len(self.list_link)):
            if self.list_link[i].event != other.list_link[i].event:
                equal = False
        return equal

    def is_final(self):
        final = True
        for link in self.list_link:
            if link.event != "ε":
                final = False
        return final

    def has_son(self, behavioral_state_final):
        son = False
        for (parent_node, transition, child_node) in behavioral_state_final:
            if self == parent_node:
                son = True
        return son
