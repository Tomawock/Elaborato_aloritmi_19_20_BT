import json
import os
import model.utility as util
import my_logger
import pickle
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
    silent_closure_space = []
    # stato inziale : behavioral_state_graph[0][0]
    silent_closure = create_silent_closure(
        behavioral_state_graph, behavioral_state_graph[0][0])
    silent_closure_space.append(silent_closure)

    for (parent_node, transition, child_node) in behavioral_state_graph:
        if transition.observable_label != 'ε':
            silent_closure = create_silent_closure(
                behavioral_state_graph, child_node)
            silent_closure_space.append(silent_closure)
    serialize_silent_closure(silent_closure_space)
    return silent_closure_space


def serialize_silent_closure(silent_closure_space):
    serialize_path="data/serialized_objects/"
    with open(os.path.join(serialize_path, "silent_closure_space"), 'wb') as f:
        #outfile=open(filename, 'wb')
        pickle.dump(silent_closure_space, f)
        #outfile.close()


def generate_diagnostic_graph(silent_space):
    diagnostic_graph = []
    for el in silent_space:
        for (p, t, c) in el.exit_transitions:
            for el2 in silent_space:
                if len(el2.sub_graph) > 0:
                    main_parent = el2.sub_graph[0][0]
                    if main_parent == c:
                        diagnostic_graph.append((el, t, el2))
                else:
                    main_parent = el2.exit_transitions[0][0]
                    if main_parent == c:
                        diagnostic_graph.append((el, t, el2))
    serialize_diagnostic_graph(diagnostic_graph)
    return diagnostic_graph

def serialize_diagnostic_graph(diagnositc_graph):
    serialize_path="data/serialized_objects/"
    with open(os.path.join(serialize_path, "diagnostic_graph"), 'wb') as f:
        #outfile=open(filename, 'wb')
        pickle.dump(diagnositc_graph, f)
        #outfile.close()


def start_execution(fa_json, transitions_json, link_original_json):
    fa_main_list = []
    transition_main_list = []
    original_link = []
    for fa in fa_json:
        fa_main_list.append(FA(fa))
    for ta in transitions_json:
        transition_main_list.append(Transition(ta))
    for li in link_original_json:
        original_link.append(Link(li["name"], li["event"]))

    util.start_timer()
    logger = my_logger.Logger.__call__().get_logger()
    logger.warning("STARTING SPAZIO_COMPORTAMENTALE")
    behavioral_state_graph, final_states = spazio_comportamentale(
        fa_main_list, transition_main_list, original_link)
    print()
    logger.warning("STARTING GENERATE_CLOSURE_SPACE")
    silent_space = generate_closure_space(behavioral_state_graph)
    for i in range(len(silent_space)):
        silent_space[i].name = i
        silent_space[i].decorate()

    logger.warning("STARTING GENERATE_DIAGNOSTIC_GRAPH")
    diagnostic_graph = generate_diagnostic_graph(silent_space)
    for (p, t, c) in diagnostic_graph:
        print("SILENT_PARENT", p.name,
              "\tTRANSITION ", t.unique_name,
              t.observable_label, t.relevant_label,
              "\tSILENT_CHILD", c.name)

def start_execution_from_serialized_behave_space(behavioral_state_graph):
    util.start_timer()
    logger=my_logger.Logger.__call__().get_logger()
    logger.warning("STARTING GENERATE_CLOSURE_SPACE")
    silent_space = generate_closure_space(behavioral_state_graph)
    for i in range(len(silent_space)):
        silent_space[i].name = i
        silent_space[i].decorate()

    logger.warning("STARTING GENERATE_DIAGNOSTIC_GRAPH")
    diagnostic_graph = generate_diagnostic_graph(silent_space)
    for (p, t, c) in diagnostic_graph:
        print("SILENT_PARENT", p.name,
              "\tTRANSITION ", t.unique_name,
              t.observable_label, t.relevant_label,
              "\tSILENT_CHILD", c.name)

def start_execution_from_serialized_silent_space(silent_space):
    util.start_timer()
    logger=my_logger.Logger.__call__().get_logger()
    logger.warning("STARTING GENERATE_DIAGNOSTIC_GRAPH")
    diagnostic_graph = generate_diagnostic_graph(silent_space)
    for (p, t, c) in diagnostic_graph:
        print("SILENT_PARENT", p.name,
              "\tTRANSITION ", t.unique_name,
              t.observable_label, t.relevant_label,
              "\tSILENT_CHILD", c.name)


if __name__ == '__main__':
    logger = my_logger.Logger("log/diagnostica").get_logger()
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

    logger.debug("STARTING SPAZIO_COMPORTAMENTALE")
    behavioral_state_graph, final_states = spazio_comportamentale(
        fa_main_list, transition_main_list, original_link)
    # silent_closure = create_silent_closure(
    #     behavioral_state_graph, behavioral_state_graph[2][0])
    # print("SILENT CLOSURE")
    # silent_closure.to_video()
    logger.debug("STARTING CLOSURE SPACE")
    silent_space = generate_closure_space(behavioral_state_graph)
    for i in range(len(silent_space)):
        silent_space[i].name = i
        silent_space[i].decorate()
        print("\nSILENT SPACE \t:",
              silent_space[i].name, "DELTA", silent_space[i].delta)
        print("EXIT TRANSICTIONS")
        for (p, t, c) in silent_space[i].exit_transitions:
            print("P:", p, "\tT:", t, "\tC:", c)

    logger.debug("STARTING DIAGNOSTIC_GRAPH")
    diagnostic_graph = generate_diagnostic_graph(silent_space)

    for (p, t, c) in diagnostic_graph:
        print("SILENT_PARENT", p.name,
              "\tTRANSITION ", t.unique_name,
              t.observable_label, t.relevant_label,
              "\tSILENT_CHILD", c.name)
