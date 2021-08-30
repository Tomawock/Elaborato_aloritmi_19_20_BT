# Pseudocodice Spazio Comportamentale

Spazio Comportamentale (FA, Transizioni, Etichette)\
**INIZIO SETUP STATO INZIALE**\
initial_state = null\
for *[PEROGNI]* FA do

if state is initial do
  * initial_state.list_fa_state <- initial_state(FA)

links <- link_univoci(Transizioni)\
initial_state.link <- links(ε) #aggiunngo per ogni link univoco il link con l'evento vuoto\
behavioral_state_queue = queue.LifoQueue()\
behavioral_state_graph = []\
behavioral_state_final = []\
snapshot = []

**FINE SETUP STATO INZIALE**\
**CREO LISTA CHE CONTIENE GLI STATI IN MODO DA POTERLI AESAMNIARE UNO ALLA VOLTA ED ESPANDERE L'ALBERO DI RICERCA**

behavioral_state_queue.put(initial_state) #LIFO QUEUE per gestire tutti i possibili statie capire quando abbiamo terminato

while(behavioral_state_queue not empty)\
behavioral_state_actual = behavioral_state_queue.pop\
**INIZIO SCELTA TRANSIZIONI ABILITATE**\
>for *[PEROGNI]* behavioral_state_actual.stati do\
possible_transitions <- bh_state.transitions
>>for possible_transition do
>>> if is_allowed(possible_transition):
        allowed_transitions.add(possible_transition)

**FINE SCELTA TRANSIZIONI ABILITATE**\

**INIZIO CAMBIO STATO FA**\
*ta* == transizione abilitata\
*fa* == Automa\
*[indice]* == posizione nella lista

* for allowed_transitions do
    next_behavioral_state = behavioral_state_actual #lo stato come quello di partenza in qaunto è lo stesso di partenza ma con minime variazioni\
    next_behavioral_state.state_list[ta.getFA].state = ta.next_state #aggiorno lo stato attuale con il suo successore rispetto alla transizione (da stato 20 passo al 21)\
    **SETTO IL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**
    * for ta_link in ta.out_link do\
      next_behavioral_state.link_list[ta_link].event = ta_link.event #setto nel next stato comportamentale l'evento di ingresso nuove in base al nome del link vecchio\
    behavioral_state_graph.add(behavioral_state_actual,ta,next_behavioral_state)

    (aggiungo in modo tale da evitare cicli ricorsivi inq aunto questo stato non dovra mai piu entrare nella lista degli stati_comportamentali *vedi t3b e nodo originale*)
    * if next_behavioral_state **non** in behavioral_state_graph
      * behavioral_state_queue.add(next_behavioral_state) #aggiungo il nuovo stato comportamentale all'insieme degli stati comportamentali

    * if next_behavioral_state.is_final() #controllo se ha eventi nulli in tutti i links
      * behavioral_state_graph.add(next_stato_comportamentale)
      snapshot.add(behavioral_state_queue,behavioral_state_final, behavioral_state_graph) #salvo lo stato generico della DFA in questo preciso istante ovvero dopo avere creato i nuovi stai terminale e non

  **FINE SETTAGGIO DEL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**\

**FINE CAMBIO STATO FA**

**INIZIO POTATURA**\
for (parent, transition, child) in behavioral_state_graph do
  * if child not in behavioral_state_final and not has_son(child)
    * remove (parent, transition, child) from behavioral_state_graph

**FINE POTATURA**\
TODO
has_figlio()\
**INIZIO RINOMINAZONE**\
behavioral_state_enumerated = behavioral_state_graph\
label <- 0\
* for (p, t, c) in behavioral_state_enumerated do
  * if found do\
  label=label +1\
  found=false
 * for (p2, t2, c2) in behavioral_state_enumerated do
    * if p==p2 do
      * if p2.name =="" do
        p2.name=label\
        found=true
    * else if p==c2 do
      * if c2.name =="" do
        c2.name=label\
        found=true
* for (p, t, c) in behavioral_state_enumerated do
  * if found do\
  label=label +1\
  found=false
  * for (p2, t2, c2) in behavioral_state_enumerated do
    * if c==c2 do
      * if c2.name =="" do
        c2.name=label\
        found=true

**FINIE RINOMINAZONE**\
TODO
get_etichetta()

## Note
**Transazioni hanno un nome univoco, partono da uno statoe ed arrivano in un'altro non puo essitere che una transizione parta da uno stato ed arrivi in 2 stati differenti**

# Struttura dati Spazio Comportamnetale

## FA
* nome_fa : String
* stati : array di stato

## Stato
* nome : String
* iniziale : bool
* transizioni_uscenti : Transizioni

## Link
* nome : String
* evento : char

## Transizione
* nome_univoco : String
* FA : String
* next_stato : String
* link_input : Link
* link_output : array di Link
* etichetta : String

## Stato comportamntale
* nome
* lista_stati_fa : array di FA
* lista_link : Array di link
