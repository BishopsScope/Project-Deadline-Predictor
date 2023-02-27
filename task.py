import pickle
import config_files as cf
from methods import *
import os

#########################################################
# THIS IS THE CLASS FOR GETTING THE INFORMATION


class Task_Information:
    def __init__(self, name, category, num_lines, num_segments, num_iterations, display_lines):
        self.name = name
        self.category = category
        self.num_lines = num_lines
        # The following variable is for storing how many segments have been completed
        # (Note: It will only be used on the front end and not the graphical plot.
        #        The graphical plot will only use num_segments)
        self.num_completed_segments = 0
        self.num_segments = num_segments
        self.num_iterations = num_iterations
        self.display_lines = display_lines

        self.filename = f"csv_files/{category}.csv"
        # self.user_input_data = np.array([])
        self.user_input_data = self.file_exists()

    def file_exists(self):
        """ Check if the file exists """

        if os.path.exists(self.filename):
            # Load previous data
            self.user_input_data = np.loadtxt(self.filename, delimiter=',')

        else:
            # Create a new array
            self.user_input_data = np.array([])

    def task_name(self):
        return self.name

    def category_type(self):
        return self.category

    def line_count(self):
        return self.num_lines

    def num_subtasks(self):
        return self.num_segments

    def decrement_subtasks(self):
        if self.num_segments != 0:
            self.num_segments -= 1

    def iterations(self):
        return self.num_iterations

    def display_plot(self):
        return self.display_lines

    def file(self):
        return self.filename

    def data(self):
        return self.user_input_data

    def set_data(self, new_data):
        self.user_input_data = new_data


class Schedule:
    def __init__(self):
        self.schedule_list = []
        self.pickle_file = "schedule/schedule.pckl"

    def add_task(self, task):
        self.schedule_list.append(task)

    def remove_task(self, task_name):

        for i in range(len(self.schedule_list)):

            if self.schedule_list[i].task_name() == task_name:

                # Remove the task with the same name as task_name
                del self.schedule_list[i]

    def start_task(self):
        pass

    def tasks(self):
        return self.schedule_list

    # TODO: Need to make this function interact with the front end
    def print_names(self):
        for task in self.schedule_list:
            print(task.task_name())

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
