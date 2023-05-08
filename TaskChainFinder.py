class TaskChainFinder:
    def __init__(self, tasks, limit_duration) :
        self.tasks = tasks
        self.limit_duration = limit_duration
        self.chains = []
        self.neighbours = [[] for i in range(len(self.tasks)+1)]
        for i in range(len(self.tasks)):
            for j in range(i+1, len(self.tasks)):
                if self.tasks[j].time_start >= self.tasks[i].time_end:
                    if(self.tasks[j].time_start - self.tasks[i].time_end) < 60:
                        self.neighbours[self.tasks[i].id ].append(self.tasks[j].copy())   
    def depth_first_search(self, current_chain, current_duration):
        current_task = current_chain[-1]
        print('current task', current_task.id, current_duration  )
        print('current chain', [task.id for task in current_chain])
        if current_duration > self.limit_duration:
            print('add')
            self.chains.append(current_chain.copy() )
            return
        for neighbour in self.neighbours[int(current_task.id)]:
            next_duration = current_duration + neighbour.time_end - neighbour.time_start
            current_chain.append(neighbour)
            self.depth_first_search(current_chain, next_duration)
            current_chain.pop()
    def solve(self):
        for task in self.tasks:
            self.depth_first_search([task], task.time_end - task.time_start)
        return self.chains
        
                