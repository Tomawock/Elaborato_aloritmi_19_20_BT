# Pseudocodice Spazio Comportamentale

Spazio Comportamentale (FA, Transizioni, Etichette)\
**INIZIO SETUP STATO INZIALE**\
Stato_comportamentale_iniziale = null\
for *[PEROGNI]* FA do
* Stato_comportamentale_iniziale.stato <- stato_iniziale(FA)

links <- link_univoci(Transizioni)\
Stato_comportamentale_iniziale.link <- links(ε) #aggiunngo per ogni link univoco il link con l'evento vuoto\
**FINE SETUP STATO INZIALE**\
**CREO LISTA CHE CONTIENE GLI STATI IN MODO DA POTERLI AESAMNIARE UNO ALLA VOLTA ED ESPANDERE L'ALBERO DI RICERCA**
stati_comportamentali.add(Stato_comportamentale_iniziale) #LIFO QUEUE per gestire tutti i possibili statie capire quando abbiamo terminato
stati_comportamentali_terminali = [] #grafo contenete tutti gli stati corretti\
stati_comportamentali_finali = [] #stati finali quelli col doppio cerchio\
snapshot = []\

while(stati_comportamentali.len != 0)\
stato_comportamentale_attuale = stati_comportamentali.pop\
**INIZIO SCELTA TRANSIZIONI ABILITATE**\
for *[PEROGNI]* stato_comportamentale_attuale.stati do\
* transizioni_possibili <- stato.transazioni


* for transizioni_possibili do
  * for stato_comportamentale_attuale.link do
    * if link.evento == .transizione_possibile.link_ingresso.evento and link.nome == transizione_possibile.link.nome\
      transizioni_abilitate <- transizione_possibile

**FINE SCELTA TRANSIZIONI ABILITATE**\

**INIZIO CAMBIO STATO FA**\
*ta* == transizione abilitata\
*fa* == Automa\
*[indice]* == posizione nella lista

* for transizioni_abilitate do
    next_stato_comportamentale = stato_comportamentale_attuale #lo stato come quello di partenza in qaunto è lo stesso di partenza ma con minime variazioni\
    next_stato_comportamentale.lista_stati[ta.getFA].stato = ta.next_stato #aggiorno lo stato attuale con il suo successore rispetto alla transizione aka da stato 20 passo al 21\
    **SETTO IL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**
    * for ta.link_uscita do\
      next_stato_comportamentale.lista_link[ta_link].evento = ta_link.evento #setto nel next stato comportamentale l'evento di ingresso nuove in base al nome del link vecchio\
    stati_comportamentali_terminali.add(stato_comportamentale_attuale,ta,next_stato_comportamentale)#aggiungo in modo tale da evitare cicli ricorsivi inq aunto questo stato non dovra mai piu entrare nella lista degli stati_comportamentali *vedi t3b e nodo originale*
    * if next_stato_comportamentale **non** presente in stati_comportamentali_terminali
      * stati_comportamentali.add(next_stato_comportamentale) #aggiungo il nuovo stato comportamentale all'insieme degli stati comportamentali
    * if next_stato_comportamentale.is_finale() #controllo se ha eventi nulli in tutti i links
      * stati_comportamentali_finali.add(next_stato_comportamentale)
      snapshot.add(stati_comportamentali,stati_comportamentali_terminali, stati_comportamentali_finali) #salvo lo stato generico della DFA in questo preciso istante ovvero dopo avere creato i nuovi stai terminale e non

  **FINE SETTAGGIO DEL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**\

**FINE CAMBIO STATO FA**

**INIZIO POTATURA**\
for (stato_padre, tranzasione, stato_figlio) in stati_comportamentali_terminali do
  * if stato_figlio not in stati_comportamentali_finali and not has_figlio(stato_figlio)
    * rimuovi (stato_padre,ta, stato_figlio) da stati_comportamentali_terminali

**FINE POTATURA**\
TODO
has_figlio()\
**INIZIO RINOMINAZONE**\
stati_comportamentali_terminali_etichettati = []\
id_univoco <- 0\
for (stato_padre, transizione, stato_figlio) stati_comportamentali_terminali do

  * if stati_comportamentali_terminali_etichettati.len >0
    * id_univoco <- stati_comportamentali_terminali_etichettati[last_posizion].get_id_figlio()\
  * etichetta <- get_etichetta(transizione, Etichette)
    stati_comportamentali_terminali_etichettati <- (stato_padre,id_univoco, tranzasione, etichetta, stato_figlio,id_univoco+1) #(stato_padre,id_univoco_padre, tranzasione, etichetta, stato_figlio,id_univoco_figlo)

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
