import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
class DrawGraph:
    def __init__(self, nodes, graph_name):
        self.nodes = nodes
        self.graph_name = graph_name
        self.arcs_dict = {}
        for node in nodes:
            for arc in node.arcs:
                self.arcs_dict[(arc.start_point, arc.end_point)] = arc

    def draw(self):
        # Draw the 
        create_graph = nx.DiGraph()
        for node in self.nodes:
            create_graph.add_node(node.id)
            for arc in node.arcs:
                create_graph.add_edge(arc.start_point, arc.end_point)
                #add directed edge
        edge_labels = dict([((n1, n2), self.arcs_dict[(n1, n2)].__repr__() )
                    for n1, n2, d in create_graph.edges(data=True)])       
        pos = nx.spring_layout(create_graph,
                                 )
        fig, ax = plt.subplots()
        nx.draw(create_graph, pos, ax=ax, with_labels=True)
        nx.drawing.nx_pylab.draw_networkx_edge_labels(create_graph, pos, edge_labels=edge_labels, ax=ax)
        plt.savefig(self.graph_name)
        plt.show()