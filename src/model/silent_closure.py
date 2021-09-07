from model.espressioni_regolari_silent import diagnosi_from_silent_closure


class SilentClosure:
    def __init__(self, name, sub_graph, exit_transitions, delta, exit_expressions):
        self.name = name
        self.sub_graph = sub_graph
        self.exit_transitions = exit_transitions
        self.delta = delta
        self.exit_expressions = exit_expressions

    def to_video(self):
        print("SUBGRAPH")
        for (p, t, c) in self.sub_graph:
            print("P:", p, "\tT:", t, "\tC:", c)
        print("EXIT TRANSITIONS")
        for (p, t, c) in self.exit_transitions:
            print("P:", p, "\tT:", t, "\tC:", c)

    # def decorate(self):
    #     for el in sub_graph:
    def get_delta_final_states(self):
        delta_final_states = []
        for (parent, t, child) in self.sub_graph:
            if parent.is_final() and parent.name not in delta_final_states:
                delta_final_states.append(parent.name)
            if child.is_final() and child.name not in delta_final_states:
                delta_final_states.append(child.name)

        return delta_final_states

    def get_exit_final_states(self):
        exit_states = []
        for (parent, t, child) in self.exit_transitions:
            if parent.name not in exit_states:
                exit_states.append(parent.name)

        return exit_states

    def decorate(self):
        delta_final_states = self.get_delta_final_states()
        print("DELTA FINAL STATE", delta_final_states)
        exit_final_states = self.get_exit_final_states()
        print("EXIT FINAL STATE", exit_final_states)

        self.delta = diagnosi_from_silent_closure(
            self.sub_graph, delta_final_states)
        self.exit_expressions = diagnosi_from_silent_closure(
            self.sub_graph, exit_final_states)
