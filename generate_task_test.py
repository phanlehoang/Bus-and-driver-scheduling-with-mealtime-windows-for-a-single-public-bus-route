import unittest
import generate_task
from generate_task import GenerateTask

class GenerateTaskTest(unittest.TestCase):
    def testGenerate(self):       
        generateTask = GenerateTask(time_begin = 360,
                                        time_finish = 60*21,
                                        step_time = 15,
                                        route_time = 60,
                                )
        tasks = generateTask.generate()
        print(tasks)
        print(len(tasks))