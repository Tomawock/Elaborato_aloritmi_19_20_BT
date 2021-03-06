import json
import os
import model.utility as util
import sys
import my_logger
import time
from memory_profiler import profile

OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def create_series_from_graph(global_sequence):
    logger = my_logger.Logger.__call__().get_logger()
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    series_sequence = []
    ordered_list = []

    for i,t,o in global_sequence:
        if i == "N0":
            ordered_list.append((i,t,o))

    for i,t,o in global_sequence:
        if i != "N0":
            ordered_list.append((i,t,o))
    global_sequence = ordered_list

    for i, t, o in global_sequence:
        series_found = 1
        in_node = i
        transaction = t
        out_node = o
        #initialize the series sequence
        series_sequence.append((in_node, transaction, out_node))
        ## Generate Series
        while(series_found == 1):
            # print("out node", out_node, "incoming", count_incoming(global_sequence, out_node),
            #       "outcoming", count_outcoming(global_sequence, out_node))
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
                    # print("Added:", series_sequence[0])
                    tmp_global.append(series_sequence[0])
                else:
                    #print("SERIED", series_sequence)
                    for el in unite_series(series_sequence):
                        tmp_global.append(el)

                for el in series_sequence:
                    # print("BANNED_LIST", banned_list)
                    banned_list.append(el)

                # print("BANNED",banned_list)
                # logger.error("BANNED LIST" + str(banned_list))
                series_sequence = []
                series_found = 0

    # print("######################")

    logger.info("DIMENSION:"+str(len(tmp_global))
                + " NEW SERIES EXECUTED:" + str(tmp_global))
    # print("FINAL_GLOBAL_SERIES", tmp_global)
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

    # print("FINAL_GLOBAL_PARALLEL", tmp_global)
    logger = my_logger.Logger.__call__().get_logger()
    logger.info("DIMENSION:"+str(len(tmp_global))
                + " NEW PARALLEL EXECUTED:" + str(tmp_global))
    return tmp_global


def create_loop_from_graph(global_sequence, n0, nq):
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    cycle_found = False
    for i, t, o in global_sequence:
        if(i != n0['name'] and o != nq['name']):
            # print("0:", i, t, o)
            for (next_in_node, next_transaction, next_out_node) in global_sequence:
                # print("1:", next_in_node, next_transaction, next_out_node)
                if (next_in_node != i and next_out_node == i):
                    # print("2:", next_in_node, next_transaction, next_out_node)
                    for (next_next_in_node, next_next_transaction, next_next_out_node) in global_sequence:

                        if (next_next_in_node == i and next_next_out_node != i):
                            if(i == o):
                                if t == NULL_SMIB and next_transaction != NULL_SMIB and next_next_transaction != NULL_SMIB:
                                    r = OPEN_BRA+next_transaction+OP_CONCAT+next_next_transaction+CLOSE_BRA
                                elif t != NULL_SMIB and next_transaction == NULL_SMIB and next_next_transaction != NULL_SMIB:
                                    r = OPEN_BRA + OPEN_BRA + t + CLOSE_BRA+OP_REP+OP_CONCAT+next_next_transaction + CLOSE_BRA
                                elif t != NULL_SMIB and next_transaction != NULL_SMIB and next_next_transaction == NULL_SMIB:
                                    r = OPEN_BRA + next_transaction+OP_CONCAT+OPEN_BRA+t + CLOSE_BRA+OP_REP + CLOSE_BRA
                                elif t == NULL_SMIB and next_transaction != NULL_SMIB and next_next_transaction == NULL_SMIB:
                                    r = OPEN_BRA + next_transaction + CLOSE_BRA
                                elif t == NULL_SMIB and next_transaction == NULL_SMIB and next_next_transaction != NULL_SMIB:
                                    r = OPEN_BRA + next_next_transaction + CLOSE_BRA
                                elif t == NULL_SMIB and next_transaction == NULL_SMIB and next_next_transaction == NULL_SMIB:
                                    r = OPEN_BRA + t + CLOSE_BRA
                                else:
                                    r = OPEN_BRA + next_transaction+OP_CONCAT+OPEN_BRA+t + \
                                    CLOSE_BRA+OP_REP+OP_CONCAT+next_next_transaction +CLOSE_BRA

                                tmp_global.append(
                                    (next_in_node, r, next_next_out_node))
                                # banned_list.append((i, t, o))
                                # banned_list.append(
                                #     (next_in_node, next_transaction, next_out_node))
                                # banned_list.append(
                                #     (next_next_in_node, next_next_transaction, next_next_out_node))
                                cycle_found = True
                            else:
                                if next_transaction == NULL_SMIB and next_next_transaction != NULL_SMIB:
                                    r = next_next_transaction
                                elif next_transaction != NULL_SMIB and next_next_transaction == NULL_SMIB:
                                    r = next_transaction
                                elif next_transaction == NULL_SMIB and next_next_transaction == NULL_SMIB:
                                    r = next_transaction
                                else:
                                    r = OPEN_BRA+next_transaction+OP_CONCAT+next_next_transaction+CLOSE_BRA

                                # print("NEXT", (next_in_node,
                                #                next_transaction, next_out_node))
                                # print("NEXT NEXT", (next_next_in_node,
                                #                     next_next_transaction, next_next_out_node))
                                # print("ORIGINAL", (i, t, o))
                                tmp_global.append(
                                    (next_in_node, r, next_next_out_node))
                                # banned_list.append(
                                #     (next_in_node, next_transaction, next_out_node))
                                # banned_list.append(
                                #     (next_next_in_node, next_next_transaction, next_next_out_node))
                                cycle_found = True

        if cycle_found:
            for p, tr, c in global_sequence:
                if p==i or c==i:
                    banned_list.append((p,tr,c))
            break

    for el in global_sequence:
        if el not in banned_list:
            tmp_global.append(el)
    #move the fist elemnt into last position in order to have the graph ordered and mantains series sequence correct
    if cycle_found:
        loop = tmp_global[0]
        tmp_global.pop(0)
        tmp_global.append(loop)
    logger = my_logger.Logger.__call__().get_logger()
    logger.info("DIMENSION:"+str(len(tmp_global))
                + " NEW LOOP EXECUTED:" + str(tmp_global))
    # print("FINAL_GLOBAL_LOOP", tmp_global)
    return tmp_global

@property
def espressione_regolare(dict):
    with open(os.path.join('data', 'stateNQ.json')) as f:
        nq = json.load(f)
    #da gestire con gli oggetti
    with open(os.path.join('data', 'stateN0.json')) as f:
        n0 = json.load(f)
    #ricerca elemnto I dentro un array di tutti i nodi
    for el in dict:
        if el['type'] == "I":
            if len(el['incomings']) > 0:
                n0['outgoings'][0]['node'] = el['name']
                dict = [n0]+dict
            else:
                n0 = el
                n0['name'] = "N0"
    stati_accettati = stati_accettazione(dict)
    if len(stati_accettati) > 1 or len(stati_accettati[0]['outgoings']) > 0:
        #aggiunte transazioni da beta0 a nq
        for el in stati_accettati:
            el['outgoings'].append(create_transaction(NULL_SMIB, nq['name']))
            el['type'] = "N"
        dict.append(nq)  # aggiungi lo stato accetato finale
    else:
        # updaet all last node names
        nq_old_name = stati_accettati[0]['name']
        for el in dict:
            for transaction in el['outgoings']:
                if transaction['node'] == nq_old_name:
                    transaction['node'] = 'NQ'

        stati_accettati[0]['name'] = 'NQ'
    for sa in stati_accettati:
        dict.append(sa)  # riaggiugi gli accettati con le nuove impostaziponi
    # print(json.dumps(dict, indent = 4))
    # #######automa definito########
    # crea albero transizioni
    logger = my_logger.Logger.__call__().get_logger()
    logger.info("DIMENSION:"+str(len(stati_accettati))
                + " ALLOWED STATES:" + str(stati_accettati))
    global_sequence = create_sequence(dict)
    # print("GLOBAL", global_sequence)
    logger.info("DIMENSION:"+str(len(global_sequence))
                + " ORIGINAL SEQUENCE:" + str(global_sequence))
    while len(global_sequence) > 1:
        global_sequence = create_series_from_graph(global_sequence)
        global_sequence = create_parallel_from_graph(global_sequence)
        global_sequence = create_loop_from_graph(global_sequence, n0, nq)

    logger.info("DIMENSION:"+str(len(global_sequence))
                + " FINAL SEQUENCE:" + str(global_sequence))
    logger.warning("REGULAR EXPRESSION:" + str(global_sequence[0][1]))


def diagnosis(observation_graph, final_states):
    # Load initial data from json files
    with open(os.path.join('data', 'stateNQ.json')) as f:
        nq = json.load(f)
    # da gestire con gli oggetti
    with open(os.path.join('data', 'stateN0.json')) as f:
        n0 = json.load(f)
    # parsing objects from observation graph into tuple array
    global_sequence = parsing(observation_graph)
    # INsert n0 in the to the first elemnt
    global_sequence = [
        ("N0", NULL_SMIB, global_sequence[0][0])] + global_sequence
    for i, t, o in observation_graph:
        for el in final_states:
            # print("FINALI:", el)
            if el == i and (i.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((i.name, NULL_SMIB, "NQ"))
            elif el == o and (o.name, NULL_SMIB, "NQ") not in global_sequence:
                global_sequence.append((o.name, NULL_SMIB, "NQ"))
    # print("GLOBAL", global_sequence)
    while len(global_sequence) > 1:
        global_sequence = create_series_from_graph(global_sequence)
        global_sequence = create_parallel_from_graph(global_sequence)
        global_sequence = create_loop_from_graph(global_sequence, n0, nq)
        # time.sleep(0.5)

    # print("FINAL_", global_sequence)
    return global_sequence


def parsing(observation_graph):
    global_sequence = []
    for i, t, o in observation_graph:
        global_sequence.append((i.name, t.relevant_label, o.name))
    return global_sequence


def unite_series(series_sequence):
    seried_sequence = []
    if len(series_sequence) >= 2:
        origin = series_sequence[0][0]
        destination = series_sequence[len(series_sequence)-1][2]
        transaction = series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            # Consente di non aggiungere le e in concatenzatione con altri simboli
            if series_sequence[i+1][1] != NULL_SMIB:
                transaction += OP_CONCAT+series_sequence[i+1][1]
        seried_sequence.append((origin, transaction, destination))
    return seried_sequence


def unite_parallel(series_sequence):
    seried_sequence = []
    if len(series_sequence) >= 2:
        origin = series_sequence[0][0]
        destination = series_sequence[len(series_sequence)-1][2]
        transaction = series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            if series_sequence[i+1][1] != NULL_SMIB:
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


def start_execution(data):
    logger = my_logger.Logger.__call__().get_logger()
    logger.debug("STARTING REGULAR EXPRESSION")
    util.start_timer()
    try:
        espressione_regolare(data)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
    except KeyboardInterrupt:
        logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
        util.stop_timer()
        logger.critical(my_logger.EXECUTION_TIME
                        + str(util.get_code_time_execution()))
        sys.exit(1)


# if __name__ == '__main__':
#     #set up logger
#     logger = my_logger.Logger("log/espressione_regolare").get_logger()
#
#     with open(os.path.join('testing_data', 'espressione_regolare.json')) as f:
#       data = json.load(f)
#
#     util.start_timer()
#     try:
#         espressione_regolare(data)
#         util.stop_timer()
#         logger.critical(my_logger.EXECUTION_TIME
#                         + str(util.get_code_time_execution()))
#     except KeyboardInterrupt:
#         logger.critical(my_logger.INTERRUPED_FROM_KEYBOARD)
#         util.stop_timer()
#         logger.critical(my_logger.EXECUTION_TIME
#                         + str(util.get_code_time_execution()))
#         sys.exit(1)
