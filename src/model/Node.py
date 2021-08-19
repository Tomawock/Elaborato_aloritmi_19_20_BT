import Type
import json
import os


class Node:
    name = ""
    type = Type.N.value  # TODOP
    outgoings = []
    incomings = []

    def __init__(self, name, type, outgoings, incomings):
        self.name = name
        self.type = type
        self.outgoings = outgoings
        self.incomings = incomings

    def create_sequence(self):
        sequence = []
        for el in dict:
            for out in self.outgoings:
                # nome nodo ingresso, trnsazione, pedice, nome nodo uscita
                sequence.append((self.name, el.transaction, el.node))
        return sequence

    # TODO: Need to be implemented
    def create_sequence_with_subscript(self):
        sequence = []
        for el in dict:
            for out in self.outgoings:
                # nome nodo ingresso, trnsazione, pedice, nome nodo uscita
                sequence.append((self.name, el.transaction, el.node))
        return sequence


if __name__ == '__main__':
    with open(os.path.join('data', 'stateNQ.json')) as f:
        nq = json.loads(f)
    Node_0 = Node(**nq)
