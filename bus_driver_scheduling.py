

class BusDriverScheduling:
    def __init__(self, drivers, tasks):
        self.drivers = drivers
        self.tasks = tasks
        self.driver_tasks = [None] + tasks + [None]
        self.model = gp.Model("bus_driver_scheduling")
        self.x = self.model.addMVar(shape=(len(drivers),
                                           len(tasks)+2,
                                           len(tasks)+2,
                                           ), vtype=GRB.BINARY, name="x")
    def select_first_task_constr(self):
        for i in range(len(self.drivers)):
            self.model.addConstr(sum(self.x[i,0,:]) <= 1)    
    def select_last_task_constr(self):
        for i in range(len(self.drivers)):
            self.model.addConstr(sum(self.x[i,:,
                                        len(self.tasks)+1]) <= 1)
    def flow_balance_constr(self):
        for d in range(len(self.drivers)):
            for i in range(1, len(self.tasks)+1):
                self.model.addConstr(sum(self.x[d,i,:]) - sum(self.x[d,:,i]) == 0)
    def select_one_task_constr(self):
        for task in range(1, len(self.tasks)+1):
            self.model.addConstr(sum(self.x[:, 1: len(task)+1,task]) == 1)
    def consecutive_task_constr(self):
        for d in range(len(self.drivers)):
            for i in range(0, len(self.tasks)+2):
                for j in range(0, len(self.tasks)+2):
                    if(i>=j):
                        self.model.addConstr(x[d,i,j]=0)
    def limit_tasks_each_driver(self):
        for d in range(len(self.drivers)):
            num_tasks = sum(self.x[d,1:len(self.tasks)+1,1:len(self.tasks)+2])
            self.model.addConstr(num_tasks >= self.drivers[d].min_tasks)
            self.model.addConstr(num_tasks <= self.drivers[d].max_tasks)
    def solve(self):
        self.consecutive_task_constr()
        self.select_first_task_constr()
        self.select_last_task_constr()
        self.select_one_task_constr()
        self.flow_balance_constr()
        self.limit_tasks_each_driver()

        
        
    
        
        
        