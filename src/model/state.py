class State:
    def __init__(self, name, initial, transitions):
        self.name = name
        self.initial = initial
        self.outgoings_transitions = transitions

    def __str__(self):
        transition = ""
        for out in self.outgoings_transitions:
            transition += out + " "
        return self.name + " " + str(self.initial) + " " + transition
