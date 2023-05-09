import gurobipy as gp
from gurobipy import GRB
import numpy as np
import datetime
from datetime import timedelta
from TaskChainFinder import TaskChainFinder
class BusDriverScheduling:
    def __init__(self, drivers, tasks):
        self.drivers = drivers
        self.tasks = tasks
        self.max_tasks_per_driver = 3
        self.max_time_per_driver = timedelta(minutes=480)
        self.max_driving_time_per_driver = timedelta(minutes=360)
        self.start_time = datetime.datetime.strptime('05:30', '%H:%M')
        self.end_time = datetime.datetime.strptime('22:00', '%H:%M')
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
                    if self.tasks[i-1].time_end > self.tasks[j-1].time_start:
                        self.model.addConstr(self.x[d,i,j]==0, name = f"consecutive_task_{d}_{i}_{j}")
    def limit_tasks_each_driver(self):
        for d in range(len(self.drivers)):
            list_variable = [self.x[d,taski,taskj]
                                 for taski in range(1, len(self.tasks)+1)
                                 for taskj in range(1, len(self.tasks)+2)]
            num_tasks = sum(list_variable)
            self.model.addConstr(num_tasks >= self.drivers[d].min_tasks, name = f"min_tasks_{d}")
            self.model.addConstr(num_tasks <= self.drivers[d].max_tasks, name = f"max_tasks_{d}")

    def task_chain_constr(self):
        #b1: tao ra task chain 
        tcf = TaskChainFinder(self.tasks, 60)
        task_chains = tcf.solve()
        #b2: tao ra cac constr tren moi chain
        for d in range (len(self.drivers)):
            for task_chain in task_chains:
                first_id = task_chain[0].id
                list_variable = [self.x[d,j, int(task_chain[0].id)] 
                                 for j in range(0, int(task_chain[0].id))]
                list_variable += [self.x[d,int(task_chain[i-1].id), int(task_chain[i].id)]
                                 for i in range(1, len(task_chain)) ]
                self.model.addConstr(sum(list_variable) <= len(task_chain)-1, name = f"task_chain_{d}_{task_chain[0].id}")
    
    
    
    def setObjective(self):
        
        ob = self.model.addVar(vtype=GRB.CONTINUOUS, name="ob")
        for d in range(len(self.drivers)):
            for i in range(1, len(self.tasks)+1):
                for j in range(1, len(self.tasks)+1):
                    if self.tasks[j-1].time_start >= self.tasks[i-1].time_end :
                            self.list_entries.append((self.tasks[j-1].time_start - self.tasks[i-1].time_end)*self.x[d,i,j])
        self.model.addConstr(gp.quicksum(self.list_entries)==ob, name = "obj")
        self.model.setObjective(ob, GRB.MINIMIZE)
    def get_solution(self):
        pass 
    def solve(self):
        self.select_first_task_constr()
        self.select_last_task_constr()
        self.select_one_task_constr()
        self.flow_balance_constr()
        self.consecutive_task_constr()
        self.limit_tasks_each_driver()
        # self.task_chain_constr()
        self.setObjective()
        self.model.optimize()
        self.get_solution()
    def easy_solve(self):
        self.select_first_task_constr()
        self.select_last_task_constr()
        self.select_one_task_constr()
        self.flow_balance_constr()
        self.consecutive_task_constr()
        self.limit_tasks_each_driver()
        # self.task_chain_constr()
        self.model.optimize()
        self.get_solution()

        

        
        
    
        
        
        