from task import Task


class GenerateTask:
    def __init__(self, time_begin, time_finish, step_time, route_time):
        # time_begin: thời gian bắt đầu : 6 h sáng
        # time_finish: thời gian kết thúc : 9 h tối
        # step_time: 15 phút 
           #nhưng sau khi 2 chiều bắt đầu đan nhau thì step_time = 30 phút
        # route_time: thời gian đi từ A->B hoặc B->A
           #sau route_time thời gian thì khoảng cách các task là step_time*2
        self.time_begin = time_begin
        self.time_finish = time_finish
        self.step_time = step_time
        self.route_time = route_time
    def generate(self):
        tasks = []
        currentTask = Task(self.time_begin, self.time_begin + self.route_time* 2)
        while (currentTask.time_end < self.time_finish):
            tasks.append(currentTask.copy())
            adjust_step_time = self.step_time
            if(currentTask.time_start >=self.time_begin + self.route_time):
                adjust_step_time = self.step_time*2                     
            currentTask = Task(currentTask.time_start + adjust_step_time,
                               currentTask.time_end + adjust_step_time)
        return tasks
        