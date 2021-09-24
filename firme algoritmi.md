## Firme Algoritmi

0 espressione_regolare --> espressione regolare di un FA

1 espressioni_regolari --> espressioni regolari in OR di un FA con multipli final states

2 spazio_comportamentale <br>
	--> INPUT: [fa_list, transition_list, original_link_list] <br>
	--> OUTPUT: [behavioral_state_graph] spazio comportamentale di una rete di FA 	 <br>

3 spazio_comportamentale_osservabile <br>
	--> INPUT: [fa_list, transition_list, original_link_list, linear_observation] <br>
	--> OUTPUT: [behavioral_state_graph (nome da cambiare in observable_graph), behavioral_state_final] <br> spazio comportamentale di una rete di FA relativo ad un'osservazione data


4 diagnosi_relativa_osservazione <br>
	--> INPUT: [observable_graph, final_states, n0, nq] observable_graph: lista di tuple che rappresentano ogni transizione (parent, transition, child) dello spazio comportamentale relativo ad un'osservazione lineare <br>
	--> OUTPUT: [global_sequence] identifica la tupla <N0, espr_regolare, NQ> <br>


5 diagnostica (nome funzione del main: generate_diagnostic_graph) <br>
	spazio_comportamentale(fa_list, transition_list, original_link_list) --> RETURN: behavioral_state_graph
	generate_closure_space(behavioral_state_graph )	--> RETURN: silent_space
	generate_diagnostic_graph(silent_space) --> RETURN: diagnostic_graph <br>
	--> INPUT: [fa_list, transition_list, original_link_list] (se cominciamo dall'inizio, altrimenti possiamo iniziare dal behavioral_state_graph, o dal silent_space <br>
	--> OUTPUT: [diagnostic_graph]


6 diagnosi_lineare <br>
	--> INPUT: [diagnostic_graph, linear_observation] <br>
	--> OUTPUT: [regular_expression] <br>
