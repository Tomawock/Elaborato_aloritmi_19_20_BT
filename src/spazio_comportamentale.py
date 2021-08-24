import json
import os
from model.fa import FA


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
        print(fa)
        fa_main_list.append(FA(fa))

    print(fa_main_list)
