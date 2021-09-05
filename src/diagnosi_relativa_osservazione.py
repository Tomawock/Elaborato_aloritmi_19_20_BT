import os
import json
import time
from model.fa import FA
from model.link import Link
from model.transition import Transition
from spazio_comportamentale_osservabile import spazio_comportamentale_osservabile


OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def create_series_from_graph(global_sequence):
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    series_sequence = []
    for i, t, o in global_sequence:
        series_found = 1
        in_node = i
        transaction = t
        out_node = o
        #initialize the series sequence
        series_sequence.append((in_node, transaction, out_node))
        ## Generate Series
        while(series_found == 1):
            if (count_incoming(global_sequence, out_node) == 1 and count_outcoming(global_sequence, out_node) == 1):
                for next_in_node, next_transaction, next_out_node in global_sequence:
                    if(next_in_node == out_node and (count_incoming(global_sequence, out_node) == 1 and count_outcoming(global_sequence, out_node) == 1)):
                        in_node = next_in_node
                        transaction = next_transaction
                        out_node = next_out_node
                        series_sequence.append(
                            (in_node, transaction, out_node))
            else:
                for el in series_sequence:
                    if el in banned_list:
                        series_sequence = []
                #add series elemnts to global
                if len(series_sequence) == 1:
                    tmp_global.append(series_sequence[0])
                else:
                    #print("SERIED",series_sequence)
                    for el in unite_series(series_sequence):
                        tmp_global.append(el)

                for el in series_sequence:
                    banned_list.append(el)
                #print("BANNED",banned_list)
                series_sequence = []
                series_found = 0
    print("FINAL_GLOBAL_SERIES", tmp_global)
    return tmp_global


def create_parallel_from_graph(global_sequence):
    parallel_sequence = []
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    #i =input node, t= transaction , o= out_node
    for i, t, o in global_sequence:
        in_node = i
        transaction = t
        out_node = o
        #initialize the series sequence
        parallel_sequence.append((in_node, transaction, out_node))
        ## Generate Series
        for (next_in_node, next_transaction, next_out_node) in global_sequence:
            if (in_node == next_in_node and out_node == next_out_node and in_node != out_node and transaction != next_transaction):
                parallel_sequence.append(
                    (next_in_node, next_transaction, next_out_node))
                in_node = next_in_node
                transaction = next_transaction
                out_node = next_out_node

        for el in parallel_sequence:
            if el in banned_list:
                parallel_sequence = []
        #add series elemnts to global
        if len(parallel_sequence) == 1:
            tmp_global.append(parallel_sequence[0])
        else:
            #print("SERIED",series_sequence)
            for el in unite_parallel(parallel_sequence):
                tmp_global.append(el)

        for el in parallel_sequence:
            banned_list.append(el)

        parallel_sequence = []

    print("FINAL_GLOBAL_PARALLEL", tmp_global)
    return tmp_global


def create_loop_from_graph(global_sequence, n0, nq):
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    cycle_found = False
    for i, t, o in global_sequence:
        if(i != n0['name'] and o != nq['name']):
            for (next_in_node, next_transaction, next_out_node) in global_sequence:
                if (next_in_node != i and next_out_node == i):
                    for (next_next_in_node, next_next_transaction, next_next_out_node) in global_sequence:
                        if (next_next_in_node == i and next_next_out_node != i):
                            if(i == o):
                                r = next_transaction+OP_CONCAT+t+OP_REP+OP_CONCAT+next_next_transaction
                                tmp_global.append(
                                    (next_in_node, r, next_next_out_node))
                                banned_list.append((i, t, o))
                                banned_list.append(
                                    (next_in_node, next_transaction, next_out_node))
                                banned_list.append(
                                    (next_next_in_node, next_next_transaction, next_next_out_node))
                                cycle_found = True
        if cycle_found:
            break

    for el in global_sequence:
        if el not in banned_list:
            tmp_global.append(el)
    #move the fist elemnt into last position in order to have the graph ordered and mantains sereis sequence correct
    loop = tmp_global[0]
    tmp_global.pop(0)
    tmp_global.append(loop)
    print("FINAL_GLOBAL_LOOP", tmp_global)
    return tmp_global


def diagnosis_from_observable(observation_graph, final_states, n0, nq):
    # parsing objects from observation graph into tuple array
    global_sequence = parsing(observation_graph)

    print("GLOBAL", global_sequence)
    for i, t, o in observation_graph:
        for el in final_states:
            if el == i and (i.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((i.name, NULL_SMIB, "NQ"))
            elif el == o and (o.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((o.name, NULL_SMIB, "NQ"))

    while len(global_sequence) > 1:
        print("START CICLO")
        global_sequence = create_series_from_graph(global_sequence)
        global_sequence = create_parallel_from_graph(global_sequence)
        global_sequence = create_loop_from_graph(global_sequence, n0, nq)
        # time.sleep(1)

    print("FINAL_", global_sequence)

# Unite sequence if oredered, it unite one sequenze of arbitrary dimension
# Prerequisite: cant contains miltiplie sequence to unite


def unite_series(series_sequence):
    seried_sequence = []
    if len(series_sequence) >= 2:
        origin = series_sequence[0][0]
        destination = series_sequence[len(series_sequence)-1][2]
        transaction = series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            transaction += OP_CONCAT+series_sequence[i+1][1]
        seried_sequence.append((origin, transaction, destination))
    return seried_sequence

# Unite sequence if oredered, it unite one sequenze of arbitrary dimension
# Prerequisite: cant contains miltiplie sequence to unite


def parsing(observation_graph):
    global_sequence = []
    for i, t, o in observation_graph:
        global_sequence.append((i.name, t.relevant_label, o.name))
    return global_sequence


def unite_parallel(series_sequence):
    seried_sequence = []
    if len(series_sequence) >= 2:
        origin = series_sequence[0][0]
        destination = series_sequence[len(series_sequence)-1][2]
        transaction = series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            transaction += OP_ALT+series_sequence[i+1][1]
        transaction = OPEN_BRA+transaction+CLOSE_BRA
        seried_sequence.append((origin, transaction, destination))
    return seried_sequence


def create_sequence(dict):
    sequence = []
    for el in dict:
        for out in el['outgoings']:
            sequence.append((el['name'], out['transaction'], out['node']))
    return sequence


def count_incoming(global_sequence, name):
    count = 0
    for in_node, transaction, out_node in global_sequence:
        if name == in_node:
            count += 1
    return count


def count_outcoming(global_sequence, name):
    count = 0
    for in_node, transaction, out_node in global_sequence:
        if name == out_node:
            count += 1
    return count


def create_transaction(transaction, node):
    new_transaction = {
        "transaction": transaction,
        "node": node
    }
    return json.dumps(new_transaction)


def stati_accettazione(dict):
    stati_accettati = []
    for el in dict:
        if el['type'] == "F":
            stati_accettati.append(el)
            dict.remove(el)
    return stati_accettati


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

    linear_observation = ['o3', 'o2', 'o2']

    observation_graph, final_states = spazio_comportamentale_osservabile(
        fa_main_list, transition_main_list, original_link, linear_observation)
    if len(observation_graph) != 0:
        diagnosis_from_observable(observation_graph, final_states, n0, nq)
    else:
        print("Observation is not correct")
