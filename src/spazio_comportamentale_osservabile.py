import json
import os
import queue
import copy
import my_logger
import sys
import pickle
import model.utility as util
from model.fa import FA
from model.link import Link
from model.transition import Transition
from model.behavioral_state import BehavioralState

NULL_SMIB = 'ε'


def spazio_comportamentale_osservabile(fa_list, transitions_list,
                                       original_link_list, linear_observation):
    logger = my_logger.Logger.__call__().get_logger()
    # print("START CREAZIONE GRAFO")
    initial_state = BehavioralState("", -1, [], [])

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

    logger.info("DIMENSION QUEUE:"+str(behavioral_state_queue.qsize())
                + " ADDED TO QUEUE:" + str(initial_state))

    while not behavioral_state_queue.empty():
        #print(behavioral_state_queue.qsize())
        #print("NEW WHILE")
        behavioral_state_actual = behavioral_state_queue.get()
        possible_transitions = []
        for (_, state) in behavioral_state_actual.list_fa_state:
            for transition_string in state.outgoings_transitions:
                for transition_object in transitions_list:
                    if transition_object.unique_name == transition_string:
                        possible_transitions.append(transition_object)

        logger.info("DIMENSION POSSIBLE TRANSITION:"
                    + str(len(possible_transitions)))
        for el in possible_transitions:
            logger.info("POSSIBLE TRANSITION "+str(el))

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
        allowed_transitions_tmp = []
        if len(linear_observation) > behavioral_state_actual.observation_index:
            for at in allowed_transitions:
                if at.observable_label != linear_observation[behavioral_state_actual.observation_index] \
                        and at.observable_label != NULL_SMIB:
                    # print("T")
                    allowed_transitions_tmp.append(at)
        elif len(linear_observation) == behavioral_state_actual.observation_index:
            for at in allowed_transitions:
                if at.observable_label != NULL_SMIB:
                    allowed_transitions_tmp.append(at)
        else:
            allowed_transitions = []

        for to_remove in allowed_transitions_tmp:
            if to_remove in allowed_transitions:
                allowed_transitions.remove(to_remove)

        logger.info("DIMENSION ALLOWED TRANSITION: "
                    + str(len(allowed_transitions)))
        for el in allowed_transitions:
            logger.info("ALLOWED TRANSITION " + str(el))

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

            #print("|DIMENSIONE CODA->", behavioral_state_queue.qsize())
            # Update index for the next_behavioral_state
            if behavioral_state_actual.observation_index < len(linear_observation)\
                    and at.observable_label == linear_observation[behavioral_state_actual.observation_index]:
                next_behavioral_state.observation_index = next_behavioral_state.observation_index + 1

                # print(
                #     "TEST:", linear_observation[behavioral_state_actual.observation_index])
            # Create graph node with transiction from parent node to child node
            behavioral_state_graph.append(
                (behavioral_state_actual, at, next_behavioral_state))

            can_add = True
            for (parent_node, transition, child_node) in behavioral_state_graph:
                if parent_node == next_behavioral_state:
                    can_add = False
                    break
            if can_add and next_behavioral_state in behavioral_state_queue.queue:
                can_add = False

            if can_add:
                behavioral_state_queue.put(next_behavioral_state)
                logger.info("FOUND NEW BEHAVIORAL STATE: "
                            + str(next_behavioral_state))

            if next_behavioral_state.is_final_obs(len(linear_observation)):
                behavioral_state_final.append(
                    next_behavioral_state)
                logger.info("FOUND NEW FINAL STATE: "
                            + str(next_behavioral_state))
            # add snapshot in order to retrive all info in case of
            # blocked by the user execution
            snapshot.append(
                (behavioral_state_graph, behavioral_state_queue, behavioral_state_final))

            logger.info("SNAPSHOT|\t|DIMENSIONE GRAFO->" + str(len(behavioral_state_graph))
                        + "\t"
                        + "|DIMENSIONE STATI FINALI->" + str(len(
                            behavioral_state_final))
                        + "\t"
                        + "|DIMENSIONE CODA->" + str(behavioral_state_queue.qsize()))

    final_states_string = ""
    for final in behavioral_state_final:
        final_states_string = final_states_string + "\n" + str(final)
    logger.info("FINAL STATES:" + final_states_string)

    logger.info("COMPLETE "+formatted_graph_labels(behavioral_state_graph))
    logger.info("DIMENSIONE GRAFO->" + str(len(behavioral_state_graph))
                + "\t"
                + "|DIMENSIONE STATI FINALI->" + str(len(
                    behavioral_state_final))
                + "\t"
                + "|DIMENSIONE CODA->" + str(behavioral_state_queue.qsize()))
    # print("STARTING PRUNING")
    pruned_touple = 0
    pruned_touple_before = -1
    while pruned_touple != pruned_touple_before:
        pruned_touple_before = pruned_touple
        for (parent_node, transition, child_node) in behavioral_state_graph:
            if (child_node not in behavioral_state_final) and (not child_node.has_son(behavioral_state_graph)):
                behavioral_state_graph.remove(
                        (parent_node, transition, child_node))
                pruned_touple += 1

    logger.warning(
        "PRUNED " + formatted_graph_labels(behavioral_state_graph))

    behavioral_state_graph = enumerate_states(
        behavioral_state_graph)

    logger.warning(
        "RENAMED " + formatted_graph_labels(behavioral_state_graph))
    serialize_object(behavioral_state_graph, behavioral_state_final)
    return behavioral_state_graph, behavioral_state_final


def serialize_object(behavioral_state_graph, behavioral_state_final):
    serialize_path = "data/serialized_objects/"
    with open(os.path.join(serialize_path, "obs_behave_state"), 'wb') as f:
        #outfile=open(filename, 'wb')
        data = (behavioral_state_graph, behavioral_state_final)
        pickle.dump(data, f)
    #outfile.close()


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


def enumerate_states_observable(behavioral_state_graph):
    behavioral_state_enumerated = copy.deepcopy(behavioral_state_graph)
    state_name = 0
    for (p, t, c) in behavioral_state_enumerated:
        for (p2, t2, c2) in behavioral_state_enumerated:
            if p == p2:
                if(p2.name == ""):
                    state_name += 1
                    p2.name = state_name
    for (p, t, c) in behavioral_state_enumerated:
        for (p2, t2, c2) in behavioral_state_enumerated:

            if(c.name == ""):
                state_name += 1
                c.name = state_name
    return behavioral_state_enumerated


def formatted_graph_labels(behavioral_state_graph):
    result = "GRAPH\t"
    for (parent_node, transition, child_node) in behavioral_state_graph:
        result = result + "PARENT_NODE:" + parent_node.observation_str() \
            + "\tTRANSITION: " + str(transition.unique_name) \
            + "\tLABEL_OBS: " + str(transition.observable_label) \
            + "\tLABEL_REL: " + str(transition.relevant_label) \
            + "\tCHILD_NODE: " + str(child_node.observation_str()) \
            + "\n"
    return result


def start_execution(fa_json, transitions_json, link_original_json, linear_observation):
    logger = my_logger.Logger.__call__().get_logger()
    logger.debug("STARTING SPAZIO COMPORTAMENTALE OSSERVABILE")
    util.start_timer()
    try:
        fa_main_list = []
        transition_main_list = []
        original_link = []
        for fa in fa_json:
            fa_main_list.append(FA(fa))
        for ta in transitions_json:
            transition_main_list.append(Transition(ta))
        for li in link_original_json:
            original_link.append(Link(li["name"], li["event"]))
        spazio_comportamentale_osservabile(
            fa_main_list, transition_main_list, original_link, linear_observation)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
    except KeyboardInterrupt:
        logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
        sys.exit(1)


if __name__ == '__main__':
    logger = my_logger.Logger(
        "log/spazio_comportamentale_osservabile").get_logger()
    with open(os.path.join('data', 'fa.json')) as f:
        fa_json = json.load(f)
    with open(os.path.join('data', 'transition.json')) as f:
        transitions_json = json.load(f)
    with open(os.path.join('data', 'original_link.json')) as f:
        link_original_json = json.load(f)
    util.start_timer()
    try:
        fa_main_list = []
        transition_main_list = []
        original_link = []
        for fa in fa_json:
            fa_main_list.append(FA(fa))
        for ta in transitions_json:
            transition_main_list.append(Transition(ta))
        for li in link_original_json:
            original_link.append(Link(li["name"], li["event"]))
        # Testing observation
        linear_observation = ['o3', 'o2', 'o3', 'o2']
        spazio_comportamentale_osservabile(
            fa_main_list, transition_main_list, original_link, linear_observation)

        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
    except KeyboardInterrupt:
        logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
        sys.exit(1)
