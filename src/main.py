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
    series_sequence=[]
    series_found=1
    for in_node,transaction,out_node in global_sequence:
        inn=in_node
        trans=transaction
        out=out_node
        while(series_found==1):
            if (count_incoming(global_sequence,out) == 1 and count_outcoming(global_sequence,out)==1): #or (count_incoming(global_sequence,inn) == 1 and count_outcoming(global_sequence,inn)==1) and is_not_in_sequence(inn,trans,out,series_sequence):
                print(global_sequence)
                print((inn,transaction,out))
                print("\n")
                #banned_sequence.append((inn,transaction,out))
                series_sequence.append((inn,transaction,out))#to test
                for next_in_node, next_transaction, next_out_node in global_sequence:
                    if(next_in_node == out_node):
                        inn=next_in_node
                        trans=next_transaction
                        out=next_out_node
                        print(out)
                #successore della tupla appena esaminata nella serie
                series_sequence.append((inn,transaction,out))
            else:
                series_found=0


    print("series found: ")
    print(series_sequence)
    print("\n")
    print("united series: ")
    print(unite_series(series_sequence))

def is_not_in_sequence(inn,trans,out,series_sequence):
    for in_node,transaction,out_node in series_sequence:
        if inn==in_node and trans==transaction and out==out_node:
            return False
    return True


#to test seems to work
def unite_series(series_sequence):
    seried_sequence=[]
    if len(series_sequence)>= 2:
        for i in range(len(series_sequence)-1):
            if series_sequence[i][2]==series_sequence[i+1][0]:
                transaction=series_sequence[i][1]+OP_CONCAT+series_sequence[i+1][1]
                origin=series_sequence[i][0]
                destination=series_sequence[i+1][2]
                seried_sequence.append((origin,transaction,destination))
    return seried_sequence

def create_sequence(dict):
    sequence=[]
    for el in dict:
        for out in el['outgoings']:
            sequence.append((el['name'],out['transaction'],out['node']))
    print(sequence)
    print("\n")
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



with open(os.path.join('data','another graph.json')) as f:
  data = json.load(f)

espressione_regolare(data)
#print(create_transaction(NULL_SMIB,3))
