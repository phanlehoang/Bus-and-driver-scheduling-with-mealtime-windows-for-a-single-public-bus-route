import gurobipy as gp
from gurobipy import GRB
import numpy as np
import timedelta
class BusDriverScheduling:
    def __init__(self, drivers, tasks):
        self.drivers = drivers
        self.tasks = tasks
        self.driver_tasks = [None] + tasks + [None]
        self.model = gp.Model("bus_driver_scheduling")
        self.x = self.model.addMVar(shape=(len(drivers),
                                           len(tasks)+2,
                                           len(tasks)+2,
                                           ), vtype=GRB.BINARY,
                                    name="x")
        self.roster = np.zeros(len(self.driver_tasks))
        self.list_entries = []
    def virtual_task_constr(self):
        for d in range(len(self.drivers)):
            self.model.addConstr(self.x[d,0,0] == 0, name = f"virtual_task_0_{d}")
            self.model.addConstr(self.x[d,len(self.tasks)+1, len(self.tasks)+1 ] == 0, name = f"virtual_task_(n+1)_{d}")
            for i in range(1, len(self.tasks)+1):
                self.model.addConstr(self.x[d,i,i] == 0, name = f"virtual_task_{i}_{d}")
    def select_first_task_constr(self):
        for i in range(len(self.drivers)):
            self.model.addConstr(sum(self.x[i,0, 1: len(self.tasks)+1]) <= 1,name = f"first_task_{i}")    
    def select_last_task_constr(self):
        for i in range(len(self.drivers)):
            self.model.addConstr(sum(self.x[i,1:len(self.tasks)+1,
                                        len(self.tasks)+1]) <= 1,name = f"last_task_{i}")
    def flow_balance_constr(self):
        for d in range(len(self.drivers)):
            for i in range(1, len(self.tasks)+1):
                self.model.addConstr(sum(self.x[d,i,:]) - sum(self.x[d,:,i]) == 0, name = f"flow_balance_{d}_{i}")
    def select_one_task_constr(self):
        for task in range(1, len(self.tasks)+1):
            list_variable = [self.x[d,taski,task] for d in range(len(self.drivers))
                          for taski in range(0, len(self.tasks)+1)]
            self.model.addConstr(sum(list_variable) == 1, name = f"select_one_task_{task}")

    def consecutive_task_constr(self):
        for d in range(len(self.drivers)):
            for i in range(1, len(self.tasks)+1):
                for j in range(1, len(self.tasks)+1):
                    if self.tasks[i-1]['time_end'] > self.tasks[j-1]['time_start']:
                        self.model.addConstr(self.x[d,i,j]==0, name = f"consecutive_task_{d}_{i}_{j}")
    def limit_tasks_each_driver(self):
        for d in range(len(self.drivers)):
            list_variable = [self.x[d,taski,taskj]
                                 for taski in range(1, len(self.tasks)+1)
                                 for taskj in range(1, len(self.tasks)+2)]
            num_tasks = sum(list_variable)
            self.model.addConstr(num_tasks >= self.drivers[d].min_tasks, name = f"min_tasks_{d}")
            self.model.addConstr(num_tasks <= self.drivers[d].max_tasks, name = f"max_tasks_{d}")
    
    def setObjective(self):
        
        ob = self.model.addVar(vtype=GRB.CONTINUOUS, name="ob")
        for d in range(len(self.drivers)):
            for i in range(1, len(self.tasks)+1):
                for j in range(1, len(self.tasks)+1):
                    if (self.tasks[j-1]['time_start'] - self.tasks[i-1]['time_end']).total_seconds() > 0:
                            self.list_entries.append((self.tasks[j-1]['time_start'] - self.tasks[i-1]['time_end']).seconds*self.x[d,i,j])
        self.model.addConstr(gp.quicksum(self.list_entries)==ob, name = "obj")
        self.model.setObjective(ob, GRB.MINIMIZE)
    
    def get_solution(self):
        pass 
    def solve(self):
        self.consecutive_task_constr()
        self.select_first_task_constr()
        self.select_last_task_constr()
        self.select_one_task_constr()
        self.flow_balance_constr()
        self.limit_tasks_each_driver()
        self.setObjective()
        self.model.optimize()
        self.get_solution()
        

        
        
    
        
        
        