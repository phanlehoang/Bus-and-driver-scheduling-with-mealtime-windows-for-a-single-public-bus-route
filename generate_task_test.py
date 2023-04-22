
import generate_task
from generate_task import GenerateTask

generateTask = GenerateTask(time_begin = 360,
                                    time_finish = 60*21,
                                    step_time = 15,
                                    route_time = 60,
                            )
tasks = generateTask.generate()
print(tasks)
print(len(tasks))