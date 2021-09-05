import json
import os

OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def create_series_from_graph(global_sequence, stati_accettati):
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    series_sequence = []
    for i, t, p, o in global_sequence:
        series_found = 1
        in_node = i
        transaction = t
        pedice = p
        out_node = o
        #initialize the series sequence
        series_sequence.append((in_node, transaction, pedice, out_node))
        ## Generate Series
        while(series_found == 1):
            if (count_incoming(global_sequence, out_node) == 1 and count_outcoming(global_sequence, out_node) == 1):
                for next_in_node, next_transaction, next_pedice, next_out_node in global_sequence:
                    if(next_in_node == out_node and (count_incoming(global_sequence, out_node) == 1 and count_outcoming(global_sequence, out_node) == 1)):
                        in_node = next_in_node
                        transaction = next_transaction
                        pedice = next_pedice
                        out_node = next_out_node
                        series_sequence.append(
                            (in_node, transaction, pedice, out_node))
            else:
                # for el in series_sequence:
                #     if el in banned_list:
                #         series_sequence = []
                #add series elemnts to global
                if len(series_sequence) == 1:
                    tmp_global.append(series_sequence[0])
                elif len(series_sequence) > 1:
                    # print("SERIED", series_sequence)
                    tmp_global.append(
                        unite_series_with_pedice(series_sequence,
                                                 stati_accettati))
                    for el in series_sequence:
                        if el in tmp_global:
                            tmp_global.remove(el)

                # for el in series_sequence:
                #     banned_list.append(el)
                # print("BANNED", banned_list)
                series_sequence = []
                series_found = 0
    #print("FINAL_GLOBAL_SERIES", tmp_global)
    return tmp_global


def create_parallel_from_graph(global_sequence):
    parallel_sequence = []
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    #i =input node, t= transaction , o= out_node
    for i, t, p, o in global_sequence:
        in_node = i
        priority = p
        transaction = t
        out_node = o
        #initialize the series sequence
        parallel_sequence.append((in_node, transaction, priority, out_node))
        ## Generate Series
        for (next_in_node, next_transaction, next_priority, next_out_node) in global_sequence:
            if (in_node == next_in_node and out_node == next_out_node and in_node != out_node and transaction != next_transaction):
                parallel_sequence.append(
                    (next_in_node, next_transaction, next_priority, next_out_node))
                in_node = next_in_node
                priority = next_priority
                transaction = next_transaction
                out_node = next_out_node

        for el in parallel_sequence:
            if el in banned_list:
                parallel_sequence = []
        # add series elemnts to global
        if len(parallel_sequence) == 1:
            tmp_global.append(parallel_sequence[0])
        elif len(parallel_sequence) > 1:
            is_joinable = True
            for i in range(len(parallel_sequence)-1):
                for j in range(i+1, len(parallel_sequence)):
                    if parallel_sequence[i][2] != parallel_sequence[j][2]:
                        is_joinable = False
            # print("SERIED",series_sequence)
            if is_joinable:
                tmp_global.append(
                    unite_parallel_with_pedice(parallel_sequence))
            else:
                for el in parallel_sequence:
                    tmp_global.append(el)
        for el in parallel_sequence:
            banned_list.append(el)

        parallel_sequence = []

    return tmp_global


def espressioni_regolari(dict):
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
                dict = [n0]+dict  # add it on first position
            else:
                n0 = el
                n0['name'] = "N0"
    stati_accettati = stati_accettazione(dict)
    # print("ACCETTATI", stati_accettati)
    # rimuovi gli stati accettati dal dict in qunato dopo verranno riaggiunti
    for el in stati_accettati:
        dict.remove(el)
    if len(stati_accettati) > 1 or len(stati_accettati[0]['outgoings']) > 0:
        # aggiunte transazioni da beta0 a nq
        for el in stati_accettati:
            el['outgoings'].append(
                (create_transaction(NULL_SMIB, nq['name'])))
        dict.append(nq)  # aggiungi lo stato accetato finale
    else:
        # updaet transaction incoming to NQ
        nq_old_name = stati_accettati[0]['name']
        for el in dict:
            for transaction in el['outgoings']:
                if transaction['node'] == nq_old_name:
                    transaction['node'] = 'NQ'

        stati_accettati[0]['name'] = 'NQ'
        stati_accettati[0]['type'] = 'AF'
    for sa in stati_accettati:
        dict.append(sa)  # riaggiugi gli accettati con le nuove impostaziponi
    ########automa definito########
    #crea albero transizioni
    # print("DICT", dict)
    global_sequence = create_sequence_with_pedice(dict)
    print("GLOBAL_", global_sequence)
    while check_number_of_states(global_sequence) \
            and check_number_of_pedici(global_sequence):

        print("###################################")
        print("START CICLO")
        global_sequence = create_series_from_graph(
            global_sequence, stati_accettati)  # usa sta  non dict
        print("FINE_ELABORAZIONE_SERIE")
        global_sequence = create_parallel_from_graph(global_sequence)
        print("FINE_ELABORAZIONE_PARALLELO")
        global_sequence = create_loop_from_graph(
            global_sequence, n0, nq, stati_accettati)
        print("FINE_ELABORAZIONE_LOOP")

    print("###################################")
    print("FINAL_", global_sequence)


def check_number_of_states(global_sequence):
    for (i, t, p, o) in global_sequence:
        if i != 'N0' or o != 'NQ':
            return True
    return False


def check_number_of_pedici(global_sequence):
    count = 0
    for (i, t, p, o) in global_sequence:
        for (ii, tt, pp, oo) in global_sequence:
            if (p == pp):
                count += 1
            if(count == 2):
                return True
        count = 0
    return False


def unite_series_with_pedice(series_sequence, stati_accettati):
    origin = series_sequence[0][0]
    destination = series_sequence[len(series_sequence)-1][3]
    transaction = series_sequence[0][1]
    for i in range(len(series_sequence)-1):
        transaction += OP_CONCAT+series_sequence[i+1][1]
    is_accettato = False
    for sa in stati_accettati:
        if sa['name'] == series_sequence[len(series_sequence)-1][0]:
            is_accettato = True
    if series_sequence[len(series_sequence)-1][3] != 'NQ' and not is_accettato:
        return (origin, transaction, -1, destination)
    elif series_sequence[len(series_sequence)-1][2] != -1:
        return (origin, transaction, series_sequence[len(series_sequence)-1][2], destination)
    else:
        return (origin, transaction, series_sequence[len(series_sequence)-1][0], destination)


def unite_parallel_with_pedice(series_sequence):
    origin = series_sequence[0][0]
    destination = series_sequence[len(series_sequence)-1][3]
    transaction = series_sequence[0][1]
    for i in range(len(series_sequence)-1):
        transaction += OP_ALT+series_sequence[i+1][1]
    transaction = OPEN_BRA+transaction+CLOSE_BRA

    return (origin, transaction, series_sequence[0][2], destination)


def create_sequence_with_pedice(dict):
    sequence = []
    for el in dict:
        for out in el['outgoings']:
            #nome nodo ingresso, trnsazione, pedice, nome nodo uscita
            sequence.append((el['name'], out['transaction'], -1, out['node']))
    return sequence


def create_loop_from_graph(global_sequence, n0, nq, stati_accettati):
    tmp_global = []  # Copy of global_sequence in order to be able to modify it
    banned_list = []  # List of elemnts in banned since already added to a list
    cycle_found = False
    for i, t, p, o in global_sequence:
        if(i != n0['name'] and o != nq['name']):
            for (next_in_node, next_transaction, next_priority, next_out_node) in global_sequence:  # (n',r',n)
                if (next_in_node != i and next_out_node == i):
                    for (next_next_in_node, next_next_transaction, next_next_priority, next_next_out_node) in global_sequence:  # è (n,r",n")
                        if (next_next_in_node == i and next_next_out_node != i and next_next_priority == -1):
                            is_accettato = False
                            for sa in stati_accettati:
                                if sa['name'] == i:
                                    is_accettato = True
                            if next_next_out_node == 'NQ' and is_accettato:
                                if(i == o):
                                    r = next_transaction+OP_CONCAT+t+OP_REP
                                    tmp_global.append(
                                        (next_in_node, r, i, next_next_out_node))
                                    cycle_found = True
                                else:
                                    r = next_transaction
                                    tmp_global.append(
                                        (next_in_node, r, i, next_next_out_node))
                                    cycle_found = True
                            elif(i == o):
                                r = next_transaction+OP_CONCAT+t+OP_REP + \
                                    OP_CONCAT+next_next_transaction
                                tmp_global.append(
                                    (next_in_node, r, -1, next_next_out_node))
                                cycle_found = True
                            else:
                                r = next_transaction+OP_CONCAT+next_next_transaction
                                tmp_global.append(
                                    (next_in_node, r, -1, next_next_out_node))
                                cycle_found = True
                            # rimuovi quelli usati per creare la nuova transaction
                            banned_list.append((i, t, p, o))
                            banned_list.append(
                                (next_in_node, next_transaction, next_priority, next_out_node))
                            banned_list.append(
                                (next_next_in_node, next_next_transaction, next_priority, next_next_out_node))
                        elif (next_next_in_node == i and next_next_out_node != i and next_next_priority != -1):
                            if(i == o):
                                r = next_transaction+OP_CONCAT+t+OP_REP + \
                                    OP_CONCAT+next_next_transaction
                                tmp_global.append(
                                    (next_in_node, r, next_next_priority, next_next_out_node))
                                cycle_found = True
                            else:
                                r = next_transaction+OP_CONCAT+next_next_transaction
                                tmp_global.append(
                                        (next_in_node, r, next_next_priority, next_next_out_node))
                                cycle_found = True
                            # rimuovi quelli usati per creare la nuova transaction
                            banned_list.append((i, t, p, o))
                            banned_list.append(
                                (next_in_node, next_transaction, next_priority, next_out_node))
                            banned_list.append(
                                (next_next_in_node, next_next_transaction, next_priority, next_next_out_node))
        if cycle_found:
            break

    for el in global_sequence:
        if el not in banned_list:
            tmp_global.append(el)
    #move the fist elemnt into last position in order to have the graph ordered and mantains sereis sequence correct
    if cycle_found:
        loop = tmp_global[0]
        tmp_global.pop(0)
        tmp_global.append(loop)
    #print("FINAL_GLOBAL_LOOP", tmp_global)
    return tmp_global


def count_incoming(global_sequence, name):
    count = 0
    for in_node, transaction, pedice, out_node in global_sequence:
        if name == in_node:
            count += 1
    return count


def count_outcoming(global_sequence, name):
    count = 0
    for in_node, transaction, pedici, out_node in global_sequence:
        if name == out_node:
            count += 1
    return count


def create_transaction(transaction, node):
    new_transaction = {
        "transaction": transaction,
        "node": node
    }
    return new_transaction


def stati_accettazione(dict):
    stati_accettati = []
    for el in dict:
        if el['type'] == "A":
            stati_accettati.append(el)
    return stati_accettati


if __name__ == '__main__':
    with open(os.path.join('data', 'espressioni_regolari.json')) as f:
        dict = json.load(f)
    espressioni_regolari(dict)
