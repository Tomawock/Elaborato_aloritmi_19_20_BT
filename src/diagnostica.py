import json
import os
from model.fa import FA
from model.link import Link
from model.transition import Transition
from model.silent_closure import SilentClosure
from spazio_comportamentale import spazio_comportamentale


def create_silent_closure(behavioral_state_graph, initial_state):
    silent_closure = SilentClosure("", [], [], "", [])
    generate_closure(
        behavioral_state_graph, initial_state, silent_closure)
    return silent_closure


def generate_closure(behavioral_state_graph, initial_state, silent_closure):
    for (parent_node, transition, child_node) in behavioral_state_graph:
        if parent_node == initial_state:
            if transition.observable_label == 'ε':
                silent_closure.sub_graph.append((
                    parent_node, transition, child_node))
                generate_closure(behavioral_state_graph,
                                 child_node, silent_closure)
            else:
                silent_closure.exit_transitions.append((
                    parent_node, transition, child_node))

    return ((None, None, None))


def generate_closure_space(behavioral_state_graph):
    slient_closure_space = []
    # stato inziale : behavioral_state_graph[0][0]
    silent_closure = create_silent_closure(
        behavioral_state_graph, behavioral_state_graph[0][0])
    slient_closure_space.append(silent_closure)

    for (parent_node, transition, child_node) in behavioral_state_graph:
        if transition.observable_label != 'ε':
            silent_closure = create_silent_closure(
                behavioral_state_graph, child_node)
            slient_closure_space.append(silent_closure)

    return slient_closure_space


if __name__ == '__main__':
    # Load initial data from json files
    with open(os.path.join('data', 'stateNQ.json')) as f:
        nq = json.load(f)
    # da gestire con gli oggetti
    with open(os.path.join('data', 'stateN0.json')) as f:
        n0 = json.load(f)
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

    behavioral_state_graph, final_states = spazio_comportamentale(
        fa_main_list, transition_main_list, original_link)
    # silent_closure = create_silent_closure(
    #     behavioral_state_graph, behavioral_state_graph[2][0])
    # print("SILENT CLOSURE")
    # silent_closure.to_video()
    silent_space = generate_closure_space(behavioral_state_graph)
    for i in range(len(silent_space)):
        silent_space[i].name = i
        silent_space[i].decorate()
        print("\nSILENT SPACE \t:",
              silent_space[i].name, "DELTA", silent_space[i].delta)
        print("EXIT TRANSICTIONS")
        for (p, t, c) in silent_space[i].exit_transitions:
            print("P:", p, "\tT:", t, "\tC:", c)
