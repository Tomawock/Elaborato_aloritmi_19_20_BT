import copy
from espressione_regolare import diagnosis

OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


class SilentClosure:
    def __init__(self, name, sub_graph, exit_transitions, delta, exit_expressions):
        self.name = name
        self.sub_graph = sub_graph  # subgraph il primo padre è il nodo d'ingresso
        # nel caso in cui sub sia nullo exit[0] è il nodo di ingresso
        self.exit_transitions = exit_transitions
        self.delta = delta
        self.exit_expressions = exit_expressions

    def to_video(self):
        print("SUBGRAPH "+str(len(self.sub_graph)))
        for (p, t, c) in self.sub_graph:
            print("P:", p, "\tT:", t, "\tC:", c)
        print("EXIT TRANSITIONS "+str(len(self.exit_transitions)))
        for (p, t, c) in self.exit_transitions:
            print("P:", p, "\tT:", t, "\tC:", c)

    def get_delta_final_states(self):
        delta_final_states = []
        for (parent, t, child) in self.sub_graph:
            if parent.is_final() and parent not in delta_final_states:
                delta_final_states.append(parent)
            if child.is_final() and child not in delta_final_states:
                delta_final_states.append(child)

        return delta_final_states

    def get_exit_final_states(self):
        exit_states = []
        for (parent, t, child) in self.exit_transitions:
            if parent not in exit_states:
                exit_states.append(parent)

        return exit_states

    def decorate(self):
        delta_final_states = self.get_delta_final_states()
        exit_final_states = self.get_exit_final_states()
        if len(self.sub_graph) > 1:
            for final_state in delta_final_states:
                # pruning
                pruned_graph = []
                pruned_graph = self.silent_prune(final_state)
                # if len(pruned_graph) > 0:
                regular_expression = diagnosis(pruned_graph, [final_state])
                self.delta = self.delta + regular_expression[0][1] + OP_ALT
            self.delta = self.delta[:-1]

            local_exit_transitions = []
            for final_state in exit_final_states:
                # pruning
                pruned_graph = []
                pruned_graph = self.silent_prune(final_state)
                # if len(pruned_graph) > 0:
                regular_expression = diagnosis(pruned_graph, [final_state])
                for i in range(len(self.exit_transitions)):
                    p = copy.deepcopy(self.exit_transitions[i][0])
                    t = copy.deepcopy(self.exit_transitions[i][1])
                    c = copy.deepcopy(self.exit_transitions[i][2])
                    if final_state == p:
                        t.relevant_label = t.relevant_label + \
                                OP_CONCAT + regular_expression[0][1]
                        # remove unused NULL_SMIB
                        t.relevant_label = t.relevant_label.replace(
                                    NULL_SMIB, '').strip()
                        if len(t.relevant_label) == 0:
                            t.relevant_label = NULL_SMIB
                        local_exit_transitions.append((p, t, c))
                self.exit_transitions = local_exit_transitions

    def silent_prune(self, final_state):
        behavioral_state_graph = copy.deepcopy(self.sub_graph)
        pruned_touple = 0
        pruned_touple_before = -1
        while pruned_touple != pruned_touple_before:
            pruned_touple_before = pruned_touple
            for (parent_node, transition, child_node) in behavioral_state_graph:
                if child_node != final_state \
                            and not child_node.has_son(behavioral_state_graph):
                    behavioral_state_graph.remove(
                            (parent_node, transition, child_node))
                    pruned_touple += 1
        return behavioral_state_graph
