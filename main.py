#import time_manager
import eel
from task import *
from computation import *


class Adapter:

    def __init__(self):

        self.schedule = Schedule()
        self.task_info1 = None

    def create_task(self, category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50):

        self.task_info1 = Task_Information(category, name, num_segments, display_lines, num_lines, num_iterations)
        self.schedule.add_task(self.task_info1)
        # print("task created")
        # print(self.schedule.list_names())
        # return self.schedule.list_names()

    def get_tasks(self):

        return self.schedule.list_names()


if __name__ == '__main__':
    eel.init("view")

    
    obj = Adapter()
    eel.expose(obj.create_task)
    eel.expose(obj.get_tasks)
    # schedule = Schedule()
    # Naming: category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50
    # task_info1 = Task_Information("Reading History", "Read history book ch 1", 5, True)
    # task_info2 = Task_Information("Writing", "Write paper for english", 5, True)
    # task_info3 = Task_Information("Research", "Writing paper for class", 5, True)
    # task_info4 = Task_Information("Running", "Laps around neighbor",  5, True)
    # task_info5 = Task_Information("Reading Math", "Read math book ch 4", 5, True)
    # print("Adding Task: " + task_info1.name)
    # schedule.add_task(task_info1)
    # schedule.add_task(task_info2)
    # schedule.add_task(task_info3)
    # schedule.add_task(task_info4)
    # schedule.add_task(task_info5)
    # schedule.print_names()

    # print(schedule.tasks())
    # schedule.add_task(task_info1)
    # print("Starting Task: " + task_info1.name)
    # schedule.start_task("Read history book ch 1")


    # task_info2 = Task_Information("Write Paper", "writing", 5, True)
    # task_info2.create_lines()
    # schedule.add_task(task_info1)
    # schedule.add_task(task_info2)
    # schedule.to_file()
    # schedule.print_names()
    # schedule.from_file()
    # schedule.remove_task(task_info1)


    # test = Computation(task_info1)
    # print(test.file_name)
    # @eel.expose
    # def create_task(category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50):
    #     # schedule.print_names()
    #     task_info1 = Task_Information(category, name, num_segments, display_lines, num_lines, num_iterations)
    #     schedule.add_task(task_info1)
    #     print("task created")
    #     print(schedule.list_names())
    #     return schedule.list_names()
    
    # @eel.expose
    # def get_tasks():

    #     return 

    eel.start("index.html",  size=(500, 500), host="127.0.0.1")
