from task import *
import numpy as np
from datetime import datetime
from sklearn import linear_model
import matplotlib.pyplot as plt
import os

DECIMAL_PLACES = 4

class Computation():

    np.set_printoptions(precision=14, suppress=True)

    def __init__(self, task):
        self.task = task
        self.lines = []
        self.start_time = None
        self.prev_time = None
        self.prev_time_mins = 0
        self.conception_time = None
        self.prev_seg = None
        self.prev_seg_mins = 0
        self.end_points = np.array([])

    def is_last_computation(self):

        return self.task.curr_subtask_num() >= self.task.num_subtasks()

    # This function should only be called once at the start
    # of the task.
    def reset_start_time(self):

        self.start_time = datetime.now()
        self.prev_time = self.start_time

    # When True, do nothing
    # When False, change the "Next Segment" button to be "Complete"
    def next_segment(self):
        if self.task.curr_subtask_num() < self.task.num_subtasks():
            self.task.update_subtask_num()
            self.running_code()
            # Convert the timedelta object to a string and format it
            return {"Number of Segments Completed: ": str(self.task.curr_subtask_num()),
                    "Start Time: ": str(self.start_time.strftime("%Y-%m-%d %H:%M:%S")),
                    "Previous Time: ": str(self.prev_time.strftime("%Y-%m-%d %H:%M:%S")),
                    "Previous Time Minutes: ": (f"{str(round(self.prev_time_mins, DECIMAL_PLACES))} minutes"),
                    "Previous Segment: ": str(self.prev_seg),
                    "Previous Segment Minutes: ": (f"{str(round(self.prev_seg_mins, DECIMAL_PLACES))} minutes"),
                    "Range: " : (f"{str(round(np.min(self.end_points), DECIMAL_PLACES))} minutes\nto\n{str(round(np.max(self.end_points), DECIMAL_PLACES))} minutes remaining")
                    }
        return {}
        
    def running_code(self):
        # Store the new prev_time and prev_seg from the newly collected segment data from the user
        # prev_time - The clock time when the last segment was completed
        # prev_seg - The time difference between the most current segment that's been completed
        #            and the one prior to that one.
        self.get_segment()

        # Note: total_seconds() converts the time difference to seconds and then we divide by 60 to convert it to mins
        # prev_seg_mins - The number of minutes between the prior and currently completed segment
        self.prev_seg_mins = self.prev_seg.total_seconds() / 60

        self.delta_time()

        # Append the newest time to our set of data we've collected
        # user_input_data - The list of segment completion times (originally generated from the CSV)
        self.task.set_data(
            np.append(self.task.data(), [self.prev_seg_mins]))

        # Train and print the new lines
        self.train_lines_2(self.task.curr_subtask_num())

        # Check if the user wants to see lines displayed or not
        if self.task.display_plot():
            # This is the first set of lines we plot
            self.plot_lines(self.task.curr_subtask_num())

        # Get the endpoints for where each line intersects the y = num_segments line
        self.retrieve_endpoints()

        # Make sure we have at least one root
        try:
            self.return_interval()

        except Exception as e:
            raise NotImplementedError()

        # Backup the current date we have in a csv file
        self.write_csv()


    def write_csv(self):
        np.savetxt(self.task.file(),
                   self.task.user_input_data, delimiter=',')

    # REMOVE CHOICE WHEN IMPLEMENTING GUI
    def get_segment(self):
        """ Get the current segment """
        # Get the current time
        self.curr_time = datetime.now()

        # Make sure that the previous time isn't AM while the old time is PM (from midnight to morning hours)
        if ((self.prev_time - self.curr_time).total_seconds() >= 0):

            self.curr_seg = self.prev_time - self.curr_time

        # Display all metrics including:
        # Previous Segment, Previous Time, Current Segment and Current Time
        # This is the case when its PM to AM
        else:
            self.curr_seg = self.curr_time - self.prev_time

        if ((self.start_time - self.curr_time).total_seconds() >= 0):
            # Conception time is the time that has elapsed
            self.conception_time = self.start_time - self.curr_time
        
        else:
            self.conception_time = self.curr_time - self.start_time

        self.prev_time = self.curr_time
        self.prev_seg = self.curr_seg

    def retrieve_endpoints(self):
        """ Retrieve the endpoints of the lines """
        self.end_points = np.array([])

        for line_index in range(len(self.lines)):

            coefficients = np.append(
                np.flip(self.lines[line_index].coef_, 0), -self.task.num_subtasks())

            coef_roots = np.roots(coefficients)

            self.end_points = np.append(self.end_points, coef_roots)

    def return_interval(self):
        """ Return the interval of the end points """
        if self.end_points.size == 0:

            raise NotImplementedError()

        else:
            self.start_time_timestamp = self.start_time.timestamp()
            self.min_end_point = np.min(self.end_points)
            self.max_end_point = np.max(self.end_points)

    def delta_time(self):
        """ Get the time difference between the start time and the previous time """

        if (self.start_time - self.prev_time).total_seconds() >= 0:

            # Get the time from inception in terms of minutes
            self.prev_time_mins = (self.start_time -
                                   self.prev_time).total_seconds() / 60

        else:

            # Get the time from inception in terms of minutes
            self.prev_time_mins = (self.prev_time -
                                   self.start_time).total_seconds() / 60

    def train_lines_2(self, curr_y_seg=0):
        """ Train the lines """
        # This is the new and improved version of train_lines. It has several improvements:
        # 1) It relies more heavily on numpy, which drastically improves speed (see plot_testing.py)
        # 2) At each segment (subtask), every separate iteration is condensed into the mean of that
        #    particular distribution. This means that when least squares is plotted it won't be as
        #    affected by the outliers of the distribution and instead focuses solely on the changing
        #    mean value as time progresses, which generates a much better prediction at the end.
        # 3) It doesn't use "dimensions", so in other words it only supports lines rather than non-linear equations

        # Generate the lines by initializing them to zero
        self.lines = [None for _ in range(self.task.line_count())]

        # Iterate through all lines
        for line in range(self.task.line_count()):

            # This is the array containing the mean of the current time at each segment's distribution
            # This allows us to calculate each iteration in parallel, which drastically speeds up the calculation
            time = np.array([0 for _ in range(self.task.iterations())])

            # total_time contains all x points for all segments generated for the current line
            total_time = np.array([])

            # total_y contains all y points for all segments generated for the current line
            total_y = np.array([])

            # This is how many segments we start at
            for segs_done in range(1, self.task.num_subtasks() + 1):

                # Update the time values by adding the mean and original time
                time = np.add(time, np.random.normal(
                    self.task.data().mean(), self.task.data().std(), self.task.iterations()))

                # This contains all x values that we use to fit the current line.
                # Note that these values are simply the mean of all iterations generated by the previous line
                x_values = np.mean(time)

                # This is just the one y-value that matches the one mean
                y_values = np.array([segs_done])

                # Add our x values to the long list of current
                total_time = np.append(total_time, x_values)
                total_y = np.append(total_y, y_values)

            # Fit the line and save it in our list of lines
            regr = linear_model.LinearRegression(fit_intercept=False)
            self.lines[line] = regr.fit(total_time.reshape(-1, 1), total_y)

            # The following line of code takes our current position in time and uses the slope
            # that was generated by fit() above to construct each line centered at our current
            # position. In other words, the following line of code is the solution to finding the
            # y intercept when you know the slope and a point.
            self.lines[line].intercept_ = curr_y_seg - \
                (self.lines[line].coef_ * self.prev_time_mins)

    def plot_lines(self, curr_y_seg=0):
        """ Plot the lines """

        # This function plots the newly formed lines after performing least squares upon the
        # completion of each segment.

        # Note: This function assumes each function is linear, so x^2, x^3 ... won't work

        # lines: a list of numpy lines
        # max_y: num_segments; the maximum y value
        # x_values: the x value of the intersection between the line y = max_y and each line

        x_values = np.array([])

        # Get all lines at the remaining indexes and save their y values when y = num_segments
        for line_index in range(len(self.lines)):

            # Note that we're appending -num_segments because we need to shift each curve down
            # by num_segments to align it with the x-axis so we can find the roots
            coefficients = np.append(np.flip(self.lines[line_index].coef_, 0), -self.task.num_subtasks())

            # Get all roots (including imaginary roots, except in this particular function there are no imaginary roots)
            coef_roots = np.roots(coefficients)

            # Append the root of the current line
            x_values = np.append(x_values, coef_roots)

        # Check if the lengths of the two arrays are the same
        if len(x_values) != len(self.lines):
            exit(1)

        # Get the maximum x value to determine the x bound for the window
        max_x = np.max(x_values)

        # Extract each line in the list of lines
        for line_index in range(len(self.lines)):

            # Note: We have two values here (our current x position in time and the x-value of where
            #       the line intersects num_segments) because we need two x points (and two y points)
            #       in order to plot a line.
            x = np.array([0, x_values[line_index]])

            # Plot the line
            plt.plot(x, self.lines[line_index].predict(x.reshape(-1, 1)))

        # Set the upper y and x bounds
        plt.xlim(0, max_x)
        plt.ylim(0, self.task.num_subtasks())
        plt.grid()
        plt.plot(self.prev_time_mins, curr_y_seg, marker="o",
                markersize=15, markeredgecolor="blue", markerfacecolor="orange")

        # Show the plot
        plt.show()