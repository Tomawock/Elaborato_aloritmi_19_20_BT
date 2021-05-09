import json
import random

OP_CONCAT=' '
OP_ALT='|'
OP_REP='*'
NULL_SMIB='ε'



def espressione_regolare(dict):
    #ricerca elemnto I dentro un array di tutti i nodi
    for el in dict:
        if el['type']=="I":
            if len(el['type'])>0:
                #da gestire con gli oggetti
                with open('data/stateN0.json') as f:
                  n0 = json.load(f)
                n0['outgoings'][0]['node']=el['name']
                dict.append(n0)
            else:
                n0=el
                n0['name']="N0"
            break
        print(el)










with open('data/graph.json') as f:
  data = json.load(f)

espressione_regolare(random.sample(data, k=len(data)))
