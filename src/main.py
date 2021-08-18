import json
import random
import os

OP_CONCAT=' '
OP_ALT='|'
OP_REP='*'
NULL_SMIB='ε'
OPEN_BRA='('
CLOSE_BRA=')'


def espressione_regolare(dict):
    with open(os.path.join('data','stateNQ.json')) as f:
        nq = json.load(f)
    #da gestire con gli oggetti
    with open(os.path.join('data','stateN0.json')) as f:
        n0 = json.load(f)

    #ricerca elemnto I dentro un array di tutti i nodi
    for el in dict:
        if el['type']=="I":
            if len(el['incomings'])>0:
                n0['outgoings'][0]['node']=el['name']
                dict.append(n0)
            else:
                n0=el
                n0['name']="N0"

    stati_accettati=stati_accettazione(dict)
    if len(stati_accettati)>1 or len(stati_accettati[0]['outgoings'])>0:
        #aggiunte transazioni da beta0 a nq
        for el in stati_accettati:
            el['outgoings'].append(create_transaction(NULL_SMIB,nq['name']))
            el['type']="N"
        dict.append(nq)#aggiungi lo stato accetato finale
    else:
        # updaet all last node names
        nq_old_name=stati_accettati[0]['name']
        for el in dict:
            for transaction in el['outgoings']:
                if transaction['node']==nq_old_name:
                    transaction['node']='NQ'

        stati_accettati[0]['name']='NQ'

    for sa in stati_accettati:
        dict.append(sa)#riaggiugi gli accettati con le nuove impostaziponi

    #print(json.dumps(dict, indent = 4))
    ########automa definito########
    #crea albero transizioni
    global_sequence=create_sequence(dict)
    tmp_global=[]           #copy of global_sequence in order to be able to modify it
    series_sequence=[]      #List of elemnts in series
    parallel_sequence=[]    #list of elemnts in parallel
    banned_list=[]          #List of elemnts in banned since already added to a list
    print("GLOBAL",global_sequence)

    # while len(global_sequence)>0:
    #     global_sequence=serie(global_sequence)
    #     if len(global_sequence)>1
    #     setta true
    #     else setta false e stopa
    #     pass
    while len(global_sequence)>1:
        print("START CICLO")
        #i =input node, t= transaction , o= out_node
        for i,t,o in global_sequence:
            series_found=1
            #print(i,t,o)
            in_node=i
            transaction=t
            out_node=o
            #initialize the series sequence
            series_sequence.append((in_node,transaction,out_node))
            ## Generate Series
            while(series_found==1):
                if (count_incoming(global_sequence,out_node) == 1 and count_outcoming(global_sequence,out_node)==1):
                    for next_in_node, next_transaction, next_out_node in global_sequence:
                        if(next_in_node == out_node and (count_incoming(global_sequence,out_node) == 1 and count_outcoming(global_sequence,out_node)==1)):
                            in_node=next_in_node
                            transaction=next_transaction
                            out_node=next_out_node
                            series_sequence.append((in_node,transaction,out_node))
                else:
                    for el in series_sequence:
                        if el in banned_list:
                            series_sequence=[]
                    #add series elemnts to global
                    if len(series_sequence)==1:
                        tmp_global.append(series_sequence[0])
                    else:
                        #print("SERIED",series_sequence)
                        for el in unite_series(series_sequence):
                            tmp_global.append(el)

                    for el in series_sequence:
                        banned_list.append(el)
                    #print("BANNED",banned_list)
                    series_sequence=[]
                    series_found=0

        global_sequence=tmp_global.copy()
        tmp_global=[]
        banned_list=[]
        print("FINAL_GLOBAL_SERIES",global_sequence)
        #Parallel
        ## Generate Parallel
        #i =input node, t= transaction , o= out_node
        for i,t,o in global_sequence:
            in_node=i
            transaction=t
            out_node=o
            #initialize the series sequence
            parallel_sequence.append((in_node,transaction,out_node))
            ## Generate Series
            for (next_in_node,next_transaction,next_out_node) in global_sequence:
                if (in_node==next_in_node and out_node==next_out_node and in_node != out_node and transaction!=next_transaction):
                    parallel_sequence.append((next_in_node,next_transaction,next_out_node))
                    in_node=next_in_node
                    transaction=next_transaction
                    out_node=next_out_node

            for el in parallel_sequence:
                if el in banned_list:
                    parallel_sequence=[]
            #add series elemnts to global
            if len(parallel_sequence)==1:
                tmp_global.append(parallel_sequence[0])
            else:
                #print("SERIED",series_sequence)
                for el in unite_parallel(parallel_sequence):
                    tmp_global.append(el)

            for el in parallel_sequence:
                banned_list.append(el)

            parallel_sequence=[]

        global_sequence=tmp_global.copy()
        tmp_global=[]
        banned_list=[]
        print("FINAL_GLOBAL_PARALLEL",global_sequence)

        cycle_found=False
        for i,t,o in global_sequence:
            #print("TEST_",n0['name']==i)
            if(i!= n0['name'] and o!=nq['name']):
                for (next_in_node,next_transaction,next_out_node) in global_sequence:
                    if (next_in_node!=i and next_out_node==i):
                        for (next_next_in_node,next_next_transaction,next_next_out_node) in global_sequence:
                            if (next_next_in_node==i and next_next_out_node!=i):
                                if(i==o):
                                    r=next_transaction+OP_CONCAT+t+OP_REP+OP_CONCAT+next_next_transaction
                                    tmp_global.append((next_in_node,r,next_next_out_node))
                                    banned_list.append((i,t,o))
                                    banned_list.append((next_in_node,next_transaction,next_out_node))
                                    banned_list.append((next_next_in_node,next_next_transaction,next_next_out_node))
                                    print("TMP",tmp_global)
                                    cycle_found=True
            if cycle_found:
                break

        #print("BANNED",banned_list)
        for el in global_sequence:
            if el not in banned_list:
                #print("ELEMNT",el)
                tmp_global.append(el)

        global_sequence=tmp_global.copy()
        tmp_global=[]
        banned_list=[]

        print("FINAL_GLOBAL_LOOP",global_sequence)

    print("FINAL_",global_sequence)

# Unite sequence if oredered, it unite one sequenze of arbitrary dimension
# Prerequisite: cant contains miltiplie sequence to unite
def unite_series(series_sequence):
    seried_sequence=[]
    if len(series_sequence)>= 2:
        origin=series_sequence[0][0]
        destination=series_sequence[len(series_sequence)-1][2]
        transaction=series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            transaction+=OP_CONCAT+series_sequence[i+1][1]
        seried_sequence.append((origin,transaction,destination))
    return seried_sequence

# Unite sequence if oredered, it unite one sequenze of arbitrary dimension
# Prerequisite: cant contains miltiplie sequence to unite
def unite_parallel(series_sequence):
    seried_sequence=[]
    if len(series_sequence)>= 2:
        origin=series_sequence[0][0]
        destination=series_sequence[len(series_sequence)-1][2]
        transaction=series_sequence[0][1]
        for i in range(len(series_sequence)-1):
            transaction+=OP_ALT+series_sequence[i+1][1]
        transaction=OPEN_BRA+transaction+CLOSE_BRA
        seried_sequence.append((origin,transaction,destination))
    return seried_sequence

def create_sequence(dict):
    sequence=[]
    for el in dict:
        for out in el['outgoings']:
            sequence.append((el['name'],out['transaction'],out['node']))
    return sequence

def count_incoming(global_sequence, name):
    count=0
    for in_node,transaction,out_node in global_sequence:
        if name == in_node:
            count+=1
    return count

def count_outcoming(global_sequence, name):
    count=0
    for in_node,transaction,out_node in global_sequence:
        if name == out_node:
            count+=1
    return count

def create_transaction(transaction, node):
    new_transaction={
        "transaction":transaction,
        "node":node
    }
    return json.dumps(new_transaction)

def stati_accettazione(dict):
    stati_accettati=[]
    for el in dict:
        if el['type']=="F":
            stati_accettati.append(el)
            dict.remove(el)
    return stati_accettati


if __name__ == '__main__':
    with open(os.path.join('data','test_graph.json')) as f:
      data = json.load(f)
    espressione_regolare(data)
#print(create_transaction(NULL_SMIB,3))
