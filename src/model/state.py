from model.transition import Transition


class State:
    def __init__(self, name, initial, transitions):
        self.name = name
        self.initial = initial
        self.outgoings_transitions = transitions
