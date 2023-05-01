class Bucket:
    def __init__(self, node_id, time):
        self.node_id = node_id
        self.time = time
    def __str__(self):
        return " Node: {}, Time: {}".format(self.node_id, self.time)
    def __repr__(self):
        return "Bucket ({}, {})".format(self.node_id, self.time)
    def copy(self):
        return Bucket(self.node_id, self.time)