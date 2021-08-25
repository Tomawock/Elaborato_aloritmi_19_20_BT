from model.state import State


class FA:

    def __init__(self, fa_name, states):
        self.fa_name = fa_name
        self.states = states

    def __init__(self, fa):
        self.fa_name = fa["name"]
        self.states = []
        for state in fa["states"]:
            self.states.append(
                State(state["name"], state["initial"],
                      state["outgoings_transitions"]))

    def __str__(self):
        string_out = self.fa_name + " "
        for el in self.states:
            string_out += str(el) + " "
        return string_out
