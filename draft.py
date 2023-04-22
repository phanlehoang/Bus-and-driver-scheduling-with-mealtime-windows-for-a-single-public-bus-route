import gurobipy as gp
from gurobipy import GRB
import numpy as np
# model = gp.Model("buffalo")
# #tao bien 3 chieu
# x = model.addMVar(shape=(3,3,3) ,vtype=GRB.BINARY, name="x")
# print(type(x))
# model.addConstr(x[0,0,0] == 1)
# model.setObjective(x[0,0,0] + x[0,0,1] + x[0,0,2], GRB.MAXIMIZE)
# model.optimize()
# #print
# for v in model.getVars():
#     print('%s %g' % (v.varName, v.x))
a = np.array([[1,2,3], [4,5,6], [7,8,9]])
print(a[0,0:2])