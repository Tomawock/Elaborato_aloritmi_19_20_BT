# Pseudocodice Spazio Comportamentale

Spazio Comportamentale (FA, Transizioni, Osservabili, Rilevanti)\
**INIZIO SETUP STATO INZIALE**\
Stato_comportamentale_iniziale = null\
for *[PEROGNI]* FA do
* Stato_comportamentale_iniziale.stato <- stato_iniziale(FA)

links <- link_univoci(Transizioni)\
Stato_comportamentale_iniziale.link <- links(ε) #aggiunngo per ogni link univoco il link con l'evento vuoto\
**FINE SETUP STATO INZIALE**\
**CREO LISTA CHE CONTIENE GLI STATI IN MODO DA POTERLI AESAMNIARE UNO ALLA VOLTA ED ESPANDERE L'ALBERO DI RICERCA**
stati_comportamentali.add(Stato_comportamentale_iniziale)\
stati_comportamentali_terminali = [] #quelli gia visitati e da non aggiungere  quelli temporanei\
stati_comportamentali_finali = [] #stati finali quelli col doppio cerchio

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
*fa.stati* == stati dell'automa

* for transizioni_abilitate do
  * for [PEROGNI] FA do
    * for fa.stati do
      * if stato.transizione == ta
        stato_comportamentale = stato_comportamentale_attuale #lo stato come quello di partenza in qaunto è lo stesso di partenza ma con minime variazioni\
        stato_comportamentale[stato] = stato.transizione.next_stato #aggiorno lo stato attuale con il suo successore rispetto allaa transizione aka da stato 20 passo al 21\
        **SETTO IL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**
        * for ta.link_uscita do\
          stato_comportamentale[ta.link_ingresso] = stato_comportamentale[link_uscita.evento] #setto nello stato comportamentale attuale l'evento di ingresso vecchio con il nuovo evento di uscita\
          stato_comportamentale_attuale.add_passo(ta,stato_comportamentale) # aggiungo l'associazione tra lo stato comportamentale e la sua transizione uscente in modo da avere l'abero per la DFA\
          stati_comportamentali_terminali.add(stato_comportamentale_attuale)#aggiungo in modo tale da evitare cicli ricorsivi inq aunto questo stato non dovra mai piuy entrare nella lista degli stati_comportamentali *vedi t3b e nodo originale*
          * if stato_comportamentale presente in stati_comportamentali_terminali
            * stati_comportamentali.add(stato_comportamentale) #aggiungo il nuovo stato comportamentale all'insieme degli stati comportamentali
          * if stato_comportamentale.is_finale() #controllo se ha eventi nulli in tutti i links
            * stati_comportamentali_finali.add(stato_comportamentale)
        * stato_generale.add(stati_comportamentali,stati_comportamentali_terminali, stati_comportamentali_finali) #salvo lo stato generico della DFA in questo preciso istante ovvero dopo avere creato i nuovi stai terminale e non
      * **FINE SETTAGGIO DEL NUOVO STATO IN BASE ALL'OUT DELLA TRANSAZIONE**\
        #Sono arrivato ad avere un array con gli stati comportamentali in base ad uno stato comportamentale di partenza, ora è necessario ciclare finchè non si è raggiunta la terminazione ovvero si è creatata la DFA
        **ATTENZIONE PUO CICLAREALL INFINITO SE NON GESTITO BENE IN QUANTO L'ALBERO è RICORSIVIO vedi t3b**
        
**FINE CAMBIO STATO FA**

**INIZIO POTATURA**
TODO
**FINE POTATURA**

**INIZIO RINOMINAZONE**
TODO
**FINIE RINOMINAZONE**













## Note
**Transazioni hanno un nome univoco**
