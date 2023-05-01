class Node:
    def __init__(self, id, arcs=[] ):
        self.id = id
        self.arcs = arcs
    def __str__(self):
        return "Node: {}, Arcs: {}".format(self.id, self.arcs)
    def __repr__(self):
        return "Node: {}, Arcs: {} \n".format(self.id, self.arcs)
    