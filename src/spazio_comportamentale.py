import json
import os
import queue
import copy
from model.fa import FA
from model.link import Link
from model.transition import Transition
from model.behavioral_state import BehavioralState


def spazio_comportamentale(fa_list, transitions_list, original_link_list):
    print("CALCOLO INIZIATO")
    initial_state = BehavioralState("", [], [])

    for fa in fa_list:
        for state in fa.states:
            if state.initial:
                initial_state.list_fa_state.append((fa.fa_name, state))
    # Stato Comp iniziale ora ha l'eleco degli sati iniziali per ogni FA
    # Aggiungo link allo stato inizale in numro pari al lìnumero di link totali
    for link in original_link_list:
        initial_state.list_link.append(link)
    # Stato iniziale
    print("STATO_INIZIALE:", str(initial_state))
    # set up queue and graph
    behavioral_state_queue = queue.LifoQueue()
    behavioral_state_visited = []
    behavioral_state_final = []
    snapshot = []

    behavioral_state_queue.put(initial_state)

    while not behavioral_state_queue.empty():
        behavioral_state_actual = behavioral_state_queue.get()
        possible_transitions = []
        for (_, state) in behavioral_state_actual.list_fa_state:
            for transition_string in state.outgoings_transitions:
                for transition_object in transitions_list:
                    if transition_object.unique_name == transition_string:
                        possible_transitions.append(transition_object)

        allowed_transitions = []
        for pt in possible_transitions:
            for link in behavioral_state_actual.list_link:
                if (link.event == pt.input_link.event
                        and link.name == pt.input_link.name) or \
                        pt.input_link.event == "" and pt.input_link.name == "":
                    allowed_transitions.append(pt)

        for at in allowed_transitions:
            next_behavioral_state = copy.deepcopy(behavioral_state_actual)
            for i in range(len(next_behavioral_state.list_fa_state)):
                (fa_name, state) = next_behavioral_state.list_fa_state[i]
                if fa_name == at.fa_name:
                    for fa in fa_list:
                        for state in fa.states:
                            if state.name == at.next_state:
                                next_behavioral_state.list_fa_state[i] = (
                                    fa_name, state)

        print("NEXT_FINALE", next_behavioral_state)
    print("CALCOLO TERMINATO")


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
    # Out to video
    for el in fa_main_list:
        print("FA", str(el))

    for el in transition_main_list:
        print("TRANSITIONS", str(el))

    spazio_comportamentale(fa_main_list, transition_main_list, original_link)
