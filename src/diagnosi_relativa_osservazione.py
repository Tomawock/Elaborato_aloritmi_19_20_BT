import os
import json
import my_logger
import model.utility as util
import pickle
from model.fa import FA
from model.link import Link
from model.transition import Transition
import espressione_regolare
from spazio_comportamentale_osservabile import spazio_comportamentale_osservabile
import sys


OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def diagnosis_from_observable(observation_graph, final_states, n0, nq):
    # parsing objects from observation graph into tuple array
    logger = my_logger.Logger.__call__().get_logger()

    global_sequence = parsing(observation_graph)

    for i, t, o in observation_graph:
        for el in final_states:
            if el == i and (i.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((i.name, NULL_SMIB, "NQ"))
            elif el == o and (o.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((o.name, NULL_SMIB, "NQ"))

    logger.info("DIMENSION:"+str(len(global_sequence))
                + " ORIGINAL SEQUENCE:" + str(global_sequence))

    # print("GLOBAL", global_sequence)

    while len(global_sequence) > 1:
        # print("START CICLO")
        global_sequence = espressione_regolare.create_series_from_graph(
            global_sequence)
        global_sequence = espressione_regolare.create_parallel_from_graph(
            global_sequence)
        global_sequence = espressione_regolare.create_loop_from_graph(
            global_sequence, n0, nq)


def parsing(observation_graph):
    global_sequence = []
    for i, t, o in observation_graph:
        global_sequence.append((i.name, t.relevant_label, o.name))
    return global_sequence


def start_execution(fa_json, transitions_json, link_original_json, linear_observation):
    logger = my_logger.Logger.__call__().get_logger()
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

        with open(os.path.join('data', 'stateNQ.json')) as f:
            nq = json.load(f)
            # da gestire con gli oggetti
        with open(os.path.join('data', 'stateN0.json')) as f:
            n0 = json.load(f)

        observation_graph, final_states = spazio_comportamentale_osservabile(
            fa_main_list, transition_main_list, original_link, linear_observation)

        if len(observation_graph) != 0:
            logger.debug("STARTING DIAGNOSIS_FROM_OBSERVABLE")
            diagnosis_from_observable(observation_graph, final_states, n0, nq)
            util.stop_timer()
        else:
            util.stop_timer()
            logger.critical("OBSERVATION: "
                            + str(linear_observation)+" IS NOT CORRECT")
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
    except KeyboardInterrupt:
        logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
        sys.exit(1)


def start_execution_from_serialized_obs_graph(observation_graph, final_states):
    logger = my_logger.Logger.__call__().get_logger()
    util.start_timer()
    try:
        with open(os.path.join('data', 'stateNQ.json')) as f:
            nq = json.load(f)
        # da gestire con gli oggetti
        with open(os.path.join('data', 'stateN0.json')) as f:
            n0 = json.load(f)

        if len(observation_graph) != 0:
            logger.debug("STARTING DIAGNOSIS_FROM_OBSERVABLE")
            diagnosis_from_observable(observation_graph, final_states, n0, nq)
            util.stop_timer()
        else:
            util.stop_timer()
            logger.error("OBSERVATION: "
                         + str(linear_observation)+" IS NOT CORRECT")
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
        "log/diagnosi_relativa_osservazione").get_logger()
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

    linear_observation = ['o3', 'o2']

    util.start_timer()
    try:
        logger.warning("LINEAR OBSERVATION:"+str(linear_observation))
        logger.debug("STARTING SPAZIO_COMPORTAMENTALE_OSSERVABILE")
        observation_graph, final_states = spazio_comportamentale_osservabile(
            fa_main_list, transition_main_list, original_link, linear_observation)
        if len(observation_graph) != 0:
            logger.debug("STARTING DIAGNOSIS_FROM_OBSERVABLE")
            diagnosis_from_observable(observation_graph, final_states, n0, nq)
            util.stop_timer()
        else:
            util.stop_timer()
            logger.critical("OBSERVATION: "
                            + str(linear_observation)+" IS NOT CORRECT")
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
    except KeyboardInterrupt:
        logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
        sys.exit(1)
