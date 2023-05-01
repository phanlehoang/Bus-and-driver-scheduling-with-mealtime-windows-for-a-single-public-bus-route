## Pseudo code of the CSP algorithm
class Arc:
    def __init__(self, cost, travel_time, start_point, end_point):
        self.cost = cost
        self.travel_time = travel_time
        self.start_point = start_point
        self.end_point = end_point
        pass
    def __str__(self):
        return "Cost: {}, Travel Time: {}".format(self.cost, self.travel_time,)
    def __repr__(self):
        return "({},{})".format(self.cost, self.travel_time,)
    # N=7
    # Node =[1,N]
