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
