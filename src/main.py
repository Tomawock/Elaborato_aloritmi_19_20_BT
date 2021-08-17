import json
import random
import os

OP_CONCAT=' '
OP_ALT='|'
OP_REP='*'
NULL_SMIB='ε'


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
    tmp_global=[]
    series_sequence=[]
    banned_list=[]
    series_found=1
    print("GLOBAL",global_sequence)

    #i =input node, t= transaction , o= out_node
    for i,t,o in global_sequence:
        series_found=1
        #print(i,t,o)
        in_node=i
        transaction=t
        out_node=o
        #initialize the series sequence
        series_sequence.append((in_node,transaction,out_node))
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

    print("FINAL_GLOBAL",tmp_global)


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



with open(os.path.join('data','graph.json')) as f:
  data = json.load(f)
espressione_regolare(data)
#print(create_transaction(NULL_SMIB,3))
