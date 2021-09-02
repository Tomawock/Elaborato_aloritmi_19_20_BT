import os
import json
from model.fa import FA
from model.link import Link
from model.transition import Transition
from src.spazio_comportamentale_osservabile import spazio_comportamentale_osservabile
from src.espressione_regolare import espressione_regolare

if __name__ == '__main__':
    with open(os.path.join('data', 'fa.json')) as f:
        fa_json = json.load(f)
    with open(os.path.join('data', 'transition.json')) as f:
        transitions_json = json.load(f)
    with open(os.path.join('data', 'original_link.json')) as f:
        link_original_json = json.load(f)
    # Creiamo gli oggetti in base la json di ingresso
    fa_main_list = []
    transition_main_list = []
    original_link = []
    for fa in fa_json:
        fa_main_list.append(FA(fa))
    for ta in transitions_json:
        transition_main_list.append(Transition(ta))
    for li in link_original_json:
        original_link.append(Link(li["name"], li["event"]))

    linear_observation = ['o3', 'o2']
    # Out to video
    print("####################INPUT DATA####################")
    for el in fa_main_list:
        print("FA", str(el))

    for el in transition_main_list:
        print("TRANSITIONS", str(el))

    for el in linear_observation:
        print("OBSERVATION", el)
    print("##################################################")
    spazio_comportamentale_osservabile(
        fa_main_list, transition_main_list, original_link, linear_observation)
