import json
import os
import queue
import copy
from model.fa import FA
from model.link import Link
from model.transition import Transition
from model.behavioral_state import BehavioralState

NULL_SMIB = 'ε'


def spazio_comportamentale_osservabile(fa_list, transitions_list, original_link_list, linear_observation):
    print("START CREAZIONE GRAFO")
    initial_state = BehavioralState("", [], [])

    for fa in fa_list:
        for state in fa.states:
            if state.initial:
                initial_state.list_fa_state.append((fa.fa_name, state))
    # Stato Comp iniziale ora ha l'eleco degli sati iniziali per ogni FA
    # Aggiungo link allo stato inizale in numro pari al lìnumero di link totali
    for link in original_link_list:
        initial_state.list_link.append(link)

    # Setto l'index dello stato iniziale a 0
    initial_state.observation_index = 0

    # Stato iniziale
    # print("STATO_INIZIALE:", str(initial_state))
    # set up queue and graph
    behavioral_state_queue = queue.LifoQueue()
    behavioral_state_graph = []
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
                        and link.name == pt.input_link.name):
                    for out_link in pt.output_link:
                        for link_beh in behavioral_state_actual.list_link:
                            if link_beh.event == NULL_SMIB and link_beh.name == out_link.name:
                                allowed_transitions.append(pt)
                    if len(pt.output_link) == 0:
                        allowed_transitions.append(pt)

                elif pt.input_link.event == "" and pt.input_link.name == "":
                    for out_link in pt.output_link:
                        for link_beh in behavioral_state_actual.list_link:
                            if link_beh.event == NULL_SMIB and link_beh.name == out_link.name:
                                allowed_transitions.append(pt)
                        if len(pt.output_link) == 0:
                            allowed_transitions.append(pt)
                    break

        # deleting not allowed transition_object
        if len(linear_observation) > behavioral_state_actual.observation_index:
            for at in allowed_transitions:
                if at.label != linear_observation[behavioral_state_actual.observation_index+1] and at.label != "":
                    allowed_transitions.remove(at)
        else:
            allowed_transitions = []

        for at in allowed_transitions:
            next_behavioral_state = copy.deepcopy(behavioral_state_actual)
            # Set up stato
            for i in range(len(next_behavioral_state.list_fa_state)):
                (fa_name, state) = next_behavioral_state.list_fa_state[i]
                if fa_name == at.fa_name:
                    for fa in fa_list:
                        for state in fa.states:
                            if state.name == at.next_state:
                                next_behavioral_state.list_fa_state[i] = (
                                    fa_name, state)
            # set up link
            for out_link in at.output_link:
                for link in next_behavioral_state.list_link:
                    if out_link.name == link.name:
                        link.swap(out_link)
                    elif at.input_link.name == link.name:
                        link.event = NULL_SMIB

            # special case of out_link empty
            if len(at.output_link) == 0:
                # print("NULL_OUT_LINK_", str(at))
                for link in next_behavioral_state.list_link:
                    if at.input_link.name == link.name:
                        link.event = NULL_SMIB

            # Create graph node with transiction from parent node to child node
            behavioral_state_graph.append(
                (behavioral_state_actual, at, next_behavioral_state))

            # can_add = True
            # for (parent_node, transition, child_node) in behavioral_state_graph:
            #     if parent_node == next_behavioral_state:
            #         can_add = False
            #         break
            #
            # if can_add:
            # Aggiungi il nuovo nodo alla coda per essere analizzato
            behavioral_state_queue.put(next_behavioral_state)

            if next_behavioral_state.is_final_obs(len(linear_observation)):
                behavioral_state_final.append(
                    next_behavioral_state)
            # add snapshot in order to retrive all info in case of
            # blocked by the user execution
            snapshot.append(
                (behavioral_state_graph, behavioral_state_queue, behavioral_state_final))
    print("END CREAZIONE GRAFO")
    print("##################################################")
    print("STATI FINALI")
    for final in behavioral_state_final:
        print(final)
    print("##################################################")
    formatted_graph_labels(behavioral_state_graph)
    print("|DIMENSIONE GRAFO->", len(behavioral_state_graph),
          "|DIMENSIONE STATI FINALI->", len(behavioral_state_final),
          "|DIMENSIONE CODA->", behavioral_state_queue.qsize())
    print("##################################################")
    print("STARTING PRUNING")
    pruned_touple = 0
    pruned_touple_before = -1
    while pruned_touple != pruned_touple_before:
        pruned_touple_before = pruned_touple
        for (parent_node, transition, child_node) in behavioral_state_graph:
            if child_node not in behavioral_state_final \
                        and not child_node.has_son(behavioral_state_graph):
                behavioral_state_graph.remove(
                        (parent_node, transition, child_node))
                pruned_touple += 1
    print("END PRUNING")
    print("##################################################")
    formatted_graph_labels(behavioral_state_graph)
    print("|DIMENSIONE GRAFO->", len(behavioral_state_graph),
          "|DIMENSIONE STATI FINALI->", len(behavioral_state_final),
          "|DIMENSIONE CODA->", behavioral_state_queue.qsize())
    print("##################################################")
    print("STARTING RENAMING")
    behavioral_state_graph = enumerate_states(behavioral_state_graph)
    print("END RENAMING")
    print("##################################################")
    formatted_graph_labels(behavioral_state_graph)
    print("|DIMENSIONE GRAFO->", len(behavioral_state_graph),
          "|DIMENSIONE STATI FINALI->", len(behavioral_state_final),
          "|DIMENSIONE CODA->", behavioral_state_queue.qsize())
    print("##################################################")
    # print("CREAZIONE IMMAGINI")
    # my_path = os.path.dirname(__file__)
    # create_pretty_graph(os.path.join(my_path, "images/"),
    #                     behavioral_state_graph)
    print("FINE ELABORAZIONE")


def enumerate_states(behavioral_state_graph):
    behavioral_state_enumerated = copy.deepcopy(behavioral_state_graph)
    label = 0
    found = False
    for (p, t, c) in behavioral_state_enumerated:
        if found:
            label += 1
            found = False
        for (p2, t2, c2) in behavioral_state_enumerated:
            if p == p2:
                if(p2.name == ""):
                    p2.name = label
                    found = True
            elif p == c2:
                if(c2.name == ""):
                    c2.name = label
                    found = True
    for (p, t, c) in behavioral_state_enumerated:
        if found:
            label += 1
            found = False
        for (p2, t2, c2) in behavioral_state_enumerated:
            if c == c2:
                if(c2.name == ""):
                    c2.name = label
                    found = True

    return behavioral_state_enumerated


def formatted_graph(behavioral_state_graph):
    print("GRAFO:")
    for (parent_node, transition, child_node) in behavioral_state_graph:
        print("PARENT_NODE ", parent_node,
              "-TRANSITION ", transition.unique_name,
              "CHILD_NODE ", child_node)


def formatted_graph_labels(behavioral_state_graph):
    print("GRAFO:")
    for (parent_node, transition, child_node) in behavioral_state_graph:
        print("PARENT_NODE:", parent_node,
              "\tTRANSITION:", transition.unique_name,
              "\tLABEL:", transition.label,
              "\tCHILD_NODE:", child_node)


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
