from typing import Type

import networkx as nx

from sinagot.base import ItemBase


class Workflow:
    graph: nx.Graph

    def __init__(self, item: Type[ItemBase]):
        self.item = item
        self._set_graph()

    def _set_graph(self) -> None:
        item = self.item
        graph = nx.DiGraph()
        graph.add_nodes_from(item._seeds)
        graph.add_nodes_from(item._steps)
        for name, step in item._steps.items():
            graph.add_edges_from(
                [
                    (source.name, name, {"label": step.func.__name__})
                    for source in step.args
                ]
            )
            graph.add_edges_from(
                [
                    (source.name, name, {"label": step.func.__name__})
                    for source in step.kwargs.values()
                ]
            )
        self.graph = graph

    def draw(self) -> None:
        graph = self.graph

        pos = nx.nx_pydot.pydot_layout(graph, prog="dot")
        edge_labels = {
            (source, dest): data["label"] for source, dest, data in graph.edges.data()
        }

        nx.draw_networkx(
            graph,
            pos=pos,
            arrows=True,
            node_color="#e1a798ff",
            font_color="#542418",
            font_weight="bold",
            node_shape="8",
            edge_color="#1a2127",
        )
        nx.draw_networkx_edge_labels(
            graph, pos=pos, edge_labels=edge_labels, rotate=False
        )
