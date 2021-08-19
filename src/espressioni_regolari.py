import json
import os

OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def create_series_from_graph(global_sequence, dict):
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
                for el in series_sequence:
                    if el in banned_list:
                        series_sequence = []
                #add series elemnts to global
                if len(series_sequence) == 1:
                    tmp_global.append(series_sequence[0])
                else:
                    # print("SERIED", series_sequence)
                    for el in unite_series_with_pedice(series_sequence, stati_accettazione(dict)):
                        tmp_global.append(el)
                    break
                for el in series_sequence:
                    banned_list.append(el)
                #print("BANNED",banned_list)
                series_sequence = []
                series_found = 0
    #print("FINAL_GLOBAL_SERIES", tmp_global)
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
    print("ACCETTATI", stati_accettati)
    if len(stati_accettati) > 1 or len(stati_accettati[0]['outgoings']) > 0:
        #aggiunte transazioni da beta0 a nq
        for el in stati_accettati:
            #PROBLEMA
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
    print("DICT", dict)
    global_sequence = create_sequence_with_pedice(dict)
    print("GLOBAL_", global_sequence)
    # check_number_of_states(global_sequence) and check_number_of_pedici(global_sequence):
    for i in range(3):
        print("START CICLO")
        global_sequence = create_series_from_graph(global_sequence, dict)
        print("FINAL_", global_sequence)

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
    seried_sequence = []
    if len(series_sequence) >= 2:
        origin = series_sequence[0][0]
        destination = series_sequence[len(series_sequence)-1][3]
        transaction = series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            transaction += OP_CONCAT+series_sequence[i+1][1]

        print("ACCETTATI_2", stati_accettati)
        is_accettato = False
        for sa in stati_accettati:
            if sa['name'] == series_sequence[len(series_sequence)-1][0]:
                is_accettato = True
        print("STATO", is_accettato)
        if series_sequence[len(series_sequence)-1][3] == 'NQ' and is_accettato:
            seried_sequence.append((origin, transaction, -1, destination))
        else:
            seried_sequence.append(
                (origin, transaction, series_sequence[len(series_sequence)-1][0], destination))
    return seried_sequence


def create_sequence_with_pedice(dict):
    sequence = []
    for el in dict:
        print("EL", el)
        for out in el['outgoings']:
            #nome nodo ingresso, trnsazione, pedice, nome nodo uscita
            sequence.append((el['name'], out['transaction'], -1, out['node']))
    return sequence


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
    return json.dumps(new_transaction)


def stati_accettazione(dict):
    stati_accettati = []
    for el in dict:
        if el['type'] == "A":
            print("CANE", el)
            stati_accettati.append(el)
            #dict.remove(el)
    return stati_accettati


if __name__ == '__main__':
    with open(os.path.join('data', 'graph_espressioni.json')) as f:
      data = json.load(f)
    #print(unite_series([('0', '(a c* b|a ε) a* c', 'NQ'), ('N0', 'ε', '0')]))
    espressioni_regolari(data)
