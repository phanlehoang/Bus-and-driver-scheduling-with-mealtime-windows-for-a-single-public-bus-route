import unittest
from bus_driver_scheduling import BusDriverScheduling
from generate_task import GenerateTask
from gurobipy import GRB
from driver import Driver
import gurobipy as gp
class BusDriverSchedulingTest(unittest.TestCase):
    def testHella(self):
        #tạo drivers
        drivers = [Driver(0,4)]*8
        #tạo tasks
        generateTask = GenerateTask(time_begin = 360,
                                        time_finish = 60*9,
                                        step_time = 15,
                                        route_time = 60,
                                )
        tasks = generateTask.generate()
        busDriverScheduling = BusDriverScheduling(drivers, tasks)
        busDriverScheduling.solve()
        print(busDriverScheduling.roster)
        #get var
        #if optimized
        model = gp.Model("buffalo")
        model.optimize()
        if busDriverScheduling.model.status == GRB.OPTIMAL:
            for v in busDriverScheduling.model.getMVars():
                print('%s %g' % (v.varName, v.x))
        else:
            print('No solution')
