import gurobipy as gp
from gurobipy import GRB

class RestrictedMasterProblem:
    def __init__(self,patterns,b,c) :
        self.patterns = patterns
        self.b = b
        self.c = c
        self.model = gp.model("restricted_master_problem")
        self.x = [self.model.addVar(vtype = GRB.CONTINUOUS, name = f"x_{i}") 
                  for i in range(len(self.c))]
    def relax_solve(self):
        self.model.setObjective(self.c @ self.x, GRB.MINIMIZE)
        self.model.addConstr(self.patterns @ self.x == self.b)
        self.model.optimize()
        return self.model.getAttr(GRB.Attr.X, self.x)