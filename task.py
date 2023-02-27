import pickle
import config_files as cf
from methods import *

#########################################################
# THIS IS THE CLASS FOR GETTING THE INFORMATION
# THIS IS CURRENTLY NOT BEING USED IN THE MAIN PORTION AND NEEDS TO BE INCLUDED


class Task_Information:
    def __init__(self, name, category, time_amt, num_lines, num_segments, num_iterations, display_lines):
        self.name = name
        self.category = category
        self.time_amt = time_amt
        self.num_lines = num_lines
        self.num_segments = num_segments
        self.num_iterations = num_iterations
        self.display_lines = display_lines

        self.filename = f"csv_files/{cf.FILE_NAME}"
        self.user_input_data = np.array([])

    def task_name(self):
        return self.name

    def create_lines(self):
        self.lines = conditions_met(self.time_amt, self.user_input_data,
                                    self.num_lines, self.num_segments, self.num_iterations)
# THIS IS A TEST FOR THE CLASS
# test = Task_Information()
# print(test.filename)
# s


class Schedule:
    def __init__(self):
        self.schedule_list = []
        self.pickle_file = "schedule/schedule.pckl"

    def add_task(self, task):
        self.schedule_list.append(task)

    def print_namees(self):
        for task in self.schedule_list:
            print(task.task_name())

    def remove_task(self, task_name):

        for i in range(len(self.schedule_list)):

            if self.schedule_list[i].task_name() == task_name:

                # Remove the task with the same name as task_name
                del self.schedule_list[i]

        # self.schedule_list.remove(task)

    def start_task(self, task):
        pass

    def to_file(self):
        """ Write schedule to pickle file """
        with open(self.pickle_file, "wb") as file_handle:
            pickle.dump(self.schedule_list, file_handle,
                        pickle.HIGHEST_PROTOCOL)

    def from_file(self):
        """Read the contents of pickle file"""
        try:
            with open(self.pickle_file, "rb") as file_handle:
                self.schedule_list = pickle.load(file_handle)
            return self.schedule_list
        except EOFError:
            return list()
