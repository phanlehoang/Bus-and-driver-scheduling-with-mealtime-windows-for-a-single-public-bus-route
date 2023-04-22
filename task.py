class Task:
    def __init__(self, time_start, time_end):
        self.time_start = time_start
        self.time_end = time_end
    def copy(self):
        return Task(self.time_start, self.time_end)
    def __repr__(self):
        return "Task: {} -> {}".format(self.time_start, self.time_end)