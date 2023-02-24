#########################################################
# THIS IS THE CLASS FOR GETTING THE INFORMATION
# THIS IS CURRENTLY NOT BEING USED IN THE MAIN PORTION AND NEEDS TO BE INCLUDED


class Task_Information:
    def __init__(self, task_name, category, time_amt, num_lines, num_segments, num_iterations, display_lines):
        self.task_name = task_name
        self.category = category
        self.time_amt = time_amt
        self.num_lines = num_lines
        self.num_segments = num_segments
        self.num_iterations = num_iterations
        self.display_lines = display_lines

        self.filename = f"csv_files/{cf.FILE_NAME}"
        self.alpha = cf.ALPHA
        self.user_input_data = np.array([])

    def create_lines(self):
        self.lines = conditions_met(self.time_amt, self.user_input_data,
                                    self.num_lines, self.num_segments, self.num_iterations)
# THIS IS A TEST FOR THE CLASS
# test = Task_Information()
# print(test.filename)
# s
