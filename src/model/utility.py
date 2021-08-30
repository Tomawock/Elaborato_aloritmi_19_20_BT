# importing networkx
import networkx as nx
# importing matplotlib.pyplot
import matplotlib.pyplot as plt
import os


def create_pretty_graph(path, behavioral_state_graph):
    graph = nx.DiGraph()
    for (parent_node, transition, child_node) in behavioral_state_graph:
        graph.add_node(parent_node.short_str())
        graph.add_node(child_node.short_str())
        graph.add_edge(parent_node.short_str(), child_node.short_str())

    # drawing in circular layout
    nx.draw_circular(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename1.png"))

    # clearing the current plot
    plt.clf()

    # drawing in planar layout
    nx.draw_planar(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename2.png"))

    # clearing the current plot
    plt.clf()

    # drawing in random layout
    nx.draw_random(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename3.png"))

    # clearing the current plot
    plt.clf()

    # drawing in spectral layout
    nx.draw_spectral(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename4.png"))

    # clearing the current plot
    plt.clf()

    # drawing in spring layout
    nx.draw_spring(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename5.png"))

    # clearing the current plot
    plt.clf()

    # drawing in shell layout
    nx.draw_shell(graph, with_labels=True, node_size=600, font_size=9)
    plt.savefig(os.path.join(path, "filename6.png"))

    # clearing the current plot
    plt.clf()
    plt.clf()
