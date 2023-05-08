class Task:
    def __init__(self,id, time_start, time_end):
        self.id = id
        self.time_start = time_start
        self.time_end = time_end
    def copy(self):
        return Task(self.id,self.time_start, self.time_end)
    def __repr__(self):
        return "Task{}: {} -> {}".format(self.id,self.time_start, self.time_end)