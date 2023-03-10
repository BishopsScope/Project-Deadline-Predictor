#import time_manager
from task import *
from computation import *

if __name__ == '__main__':
    schedule = Schedule()
    # Naming: category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50
    task_info1 = Task_Information("Reading History", "Read history book ch 1", 5, True)
    # task_info2 = Task_Information("Writing", "Write paper for english", 5, True)
    # task_info3 = Task_Information("Research", "Writing paper for class", 5, True)
    # task_info4 = Task_Information("Running", "Laps around neighbor",  5, True)
    # task_info5 = Task_Information("Reading Math", "Read math book ch 4", 5, True)
    print("Adding Task: " + task_info1.name)
    schedule.add_task(task_info1)
    # schedule.add_task(task_info2)
    # schedule.add_task(task_info3)
    # schedule.add_task(task_info4)
    # schedule.add_task(task_info5)
    # schedule.print_names()

    # print(schedule.tasks())
    # schedule.add_task(task_info1)
    print("Starting Task: " + task_info1.name)
    schedule.start_task("Read history book ch 1")


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
