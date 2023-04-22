import gurobipy as gp
from gurobipy import GRB
import numpy as np
model = gp.Model("buffalo")
#tao bien 3 chieu
x = model.addMVar(shape=(3,3,3) ,vtype=GRB.BINARY, name="x")
print(type(x))
list_Entry = []
list_Entry.append(x[0,0,1]*2)
model.addConstr(sum(list_Entry) <= 1)
model.setObjective(sum(x[:,1,2]), GRB.MAXIMIZE)
model.optimize()
#print
for v in model.getVars():
    print('%s %g' % (v.varName, v.x))
