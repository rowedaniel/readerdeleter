import matplotlib.pyplot as plt
from networkx import DiGraph, draw, draw_networkx_edge_labels, bfs_layout

from readerdeleter.build.dafsa import DAFSA


def populate_graph(
    graph: DiGraph, dafsa: DAFSA, string: str = "", parent: int = 0
) -> int:
    if parent == 0:
        graph.add_node(0, terminal=dafsa.is_word(""))

    for next_character, node_id in dafsa.next_characters(string).items():
        graph.add_node(node_id, terminal=dafsa.is_word(string + next_character))
        graph.add_edge(parent, node_id, label=next_character)

        populate_graph(graph, dafsa, string + next_character, node_id)


def draw_graph(dafsa: DAFSA, ax):
    graph = DiGraph()
    populate_graph(graph, dafsa)
    edge_labels = {edge: graph.edges[edge]["label"] for edge in graph.edges()}
    node_colors = [
        "red" if node == 0 else ("green", "blue")[graph.nodes[node]["terminal"]]
        for node in graph.nodes()
    ]

    pos = bfs_layout(graph, 0)
    draw(graph, pos=pos, node_color=node_colors, ax=ax)
    draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels, ax=ax)


def main():
    dafsa = DAFSA()
    words = [
        "CAT",
        "CART",
        "SMART",
        "ART",
        "BAD",
    ]
    words.sort()

    axs = []
    for i in range(0, len(words), 2):
        _, axs1 = plt.subplots(1, 2)
        axs.extend(axs1)

    for i,word in enumerate(words):
        dafsa.add_word(word)

        ax = axs[i]
        draw_graph(dafsa, ax)
        ax.set_title(i)

    dafsa.finish()

    ax = axs[len(words)]
    draw_graph(dafsa, ax)
    ax.set_title(i)
    


    plt.show()


if __name__ == "__main__":
    main()
