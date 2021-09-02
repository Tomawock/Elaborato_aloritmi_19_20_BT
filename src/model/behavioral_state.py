from model.link import Link
from model.fa import FA


class BehavioralState:
    def __init__(self, name, observation_index, list_fa_state, list_link):
        self.name = name
        self.observation_index = observation_index
        self.list_fa_state = list_fa_state
        self.list_link = list_link

    def __str__(self):
        string_out = "(RENAMED:" + str(self.name) + "|STATI:"
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + ","
        string_out = string_out[:-1]  # remove last virgola
        string_out += "|EVENTI:"
        for link in self.list_link:
            string_out += link.event + ","
        string_out = string_out[:-1]
        return string_out + ")"

    def short_str(self):
        string_out = "(" + str(self.name) + "|"
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + "|"
        string_out += "|"
        for link in self.list_link:
            string_out += link.event + "|"

        return string_out + ")"

    def observation_str(self):
        string_out = "(RENAMED:" + str(self.name) + \
                       "|OBS INDEX " + str(self.observation_index) + "|STATI:"
        for tuple_state in self.list_fa_state:
            string_out += str(tuple_state[1].name) + ","
        string_out = string_out[:-1]  # remove last virgola
        string_out += "|EVENTI:"
        for link in self.list_link:
            string_out += link.event + ","
        string_out = string_out[:-1]
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
        if self.observation_index != other.observation_index:
            equal = False
        return equal

    def is_final(self):
        final = True
        for link in self.list_link:
            if link.event != "ε":
                final = False
        return final

    def is_final_obs(self, max_dim):
        final = True
        for link in self.list_link:
            if link.event != "ε" or self.observation_index != max_dim:
                final = False
        return final

    def has_son(self, behavioral_state_final):
        son = False
        for (parent_node, transition, child_node) in behavioral_state_final:
            if self == parent_node:
                son = True
        return son
