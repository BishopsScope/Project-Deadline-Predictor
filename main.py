#import time_manager
from task import *
from computation import *

if __name__ == '__main__':
    schedule = Schedule()
    task_info1 = Task_Information("Read Book", "reading", 5, True)
    task_info2 = Task_Information("Write Paper", "writing", 5, True)
    task_info3 = Task_Information("Running", "laps", 5, True)
    schedule.add_task(task_info1)
    schedule.add_task(task_info2)
    schedule.add_task(task_info3)
    schedule.remove_task("Read Book")
    schedule.print_names()

    # print(schedule.tasks())
    # schedule.add_task(task_info1)
    # schedule.start_task("Read Book")


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
