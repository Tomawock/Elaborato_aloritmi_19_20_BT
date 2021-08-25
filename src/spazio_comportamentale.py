import json
import os
from model.fa import FA
from model.transition import Transition


def spazio_comportamentale(fa, transitions, labels):

    pass


if __name__ == '__main__':
    with open(os.path.join('data', 'fa.json')) as f:
        fa_json = json.load(f)
    with open(os.path.join('data', 'transition.json')) as f:
        transitions_json = json.load(f)
    # Creiamo gli oggetti in base la json di ingresso
    fa_main_list = []
    for fa in fa_json:
        fa_main_list.append(FA(fa))

    transition_main_list = []
    for ta in transitions_json:
        transition_main_list.append(Transition(ta))

    # Out to video
    for el in fa_main_list:
        print("SINGOLA_FA", str(el))

    for el in transition_main_list:
        print("Transition", str(el))
