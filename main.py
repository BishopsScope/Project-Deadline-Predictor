import eel
from task import *
from computation import *

class Adapter:

    def __init__(self):

        self.schedule = Schedule()
        self.task_info1 = None
        self.computation = None

    def create_task(self, category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50):
        self.task_info1 = Task_Information(str(category), str(name), int(num_segments), display_lines, int(num_lines), int(num_iterations))
        self.schedule.add_task(self.task_info1)

    def get_tasks(self):

        return self.schedule.list_names()

    def delete_task(self, task_name):

        self.schedule.remove_task(task_name)

    def setup_computation(self, task_name):

        self.computation = self.schedule.setup_computation(task_name)

    def check_last_computation(self):

        return self.computation.is_last_computation()

    def reset_time(self):

        self.computation.reset_start_time()

    def next_segment(self):
        return self.computation.next_segment()

    def update_pickle(self):
        self.schedule.to_file()

if __name__ == '__main__':
    eel.init("view")

    
    obj = Adapter()
    eel.expose(obj.create_task)
    eel.expose(obj.get_tasks)
    eel.expose(obj.delete_task)
    eel.expose(obj.setup_computation)
    eel.expose(obj.reset_time)
    eel.expose(obj.next_segment)
    eel.expose(obj.check_last_computation)
    eel.expose(obj.update_pickle)

    eel.start("index.html",  size=(500, 550), host="127.0.0.1")