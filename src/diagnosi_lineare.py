import json
import os
from model.fa import FA
from model.link import Link
from model.transition import Transition
from model.silent_closure import SilentClosure
from spazio_comportamentale import spazio_comportamentale
from diagnostica import generate_closure_space, generate_diagnostic_graph

OP_CONCAT = ' '
OP_ALT = '|'
OP_REP = '*'
NULL_SMIB = 'ε'
OPEN_BRA = '('
CLOSE_BRA = ')'


def generate_linear_diagnostic(diagnostic_graph, linear_observation):
    X = [(diagnostic_graph[0][0], diagnostic_graph[0][1].relevant_label)]
    for o in linear_observation:
        X_new = []
        for (x1, p1) in X:
            for (p, t, c) in diagnostic_graph:
                if p == x1:
                    p2 = p1+OP_CONCAT+t.relevant_label
                    found = False
                    for (x2_primo, p2_primo) in X_new:
                        if x2_primo == c:
                            found = True
                            p2_primo = p2_primo+OP_ALT+p2
                            break
                    if not found:
                        X_new.append((c, p2))
        X = X_new
    for (x, p) in X:
        if x.delta == "":
            X.remove((x, p))
    R = ""
    print("GRANDE", len(X))
    if len(X) == 1:
        R = X[0][1] + OP_CONCAT + X[0][0].delta
    elif len(X) > 1:
        for (x, p) in X:
            R = R + OPEN_BRA + p + OPEN_BRA + \
                 x.delta+CLOSE_BRA+CLOSE_BRA + OP_ALT
        X = X[:-1]
    return R


if __name__ == '__main__':
    # Load initial data from json files
    with open(os.path.join('data', 'stateNQ.json')) as f:
        nq = json.load(f)
    # da gestire con gli oggetti
    with open(os.path.join('data', 'stateN0.json')) as f:
        n0 = json.load(f)
    with open(os.path.join('data', 'fa.json')) as f:
        fa_json = json.load(f)
    with open(os.path.join('data', 'transition.json')) as f:
        transitions_json = json.load(f)
    with open(os.path.join('data', 'original_link.json')) as f:
        link_original_json = json.load(f)
    # Creiamo gli oggetti in base la json di ingresso
    fa_main_list = []
    transition_main_list = []
    original_link = []
    for fa in fa_json:
        fa_main_list.append(FA(fa))
    for ta in transitions_json:
        transition_main_list.append(Transition(ta))
    for li in link_original_json:
        original_link.append(Link(li["name"], li["event"]))

    behavioral_state_graph, final_states = spazio_comportamentale(
        fa_main_list, transition_main_list, original_link)
    # silent_closure = create_silent_closure(
    #     behavioral_state_graph, behavioral_state_graph[2][0])
    # print("SILENT CLOSURE")
    # silent_closure.to_video()
    silent_space = generate_closure_space(behavioral_state_graph)
    for i in range(len(silent_space)):
        silent_space[i].name = i
        silent_space[i].decorate()

    diagnostic_graph = generate_diagnostic_graph(silent_space)

    for (p, t, c) in diagnostic_graph:
        print("SILENT_PARENT", p.name,
              "\tTRANSITION ", t.unique_name,
              t.observable_label, t.relevant_label,
              "\tSILENT_CHILD", c.name)

    linear_observation = ['o3', 'o2', 'o3', 'o2']
    r = generate_linear_diagnostic(diagnostic_graph, linear_observation)
    print("FINEEEE\t", r)
