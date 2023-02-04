import numpy as np
import matplotlib.pyplot as plt
import random as rand
from sklearn import linear_model
from datetime import datetime
import time
import os
from methods import *
import decimal


def running_code():

    # INSERT CONFIG
    filename = 'data.csv'

    # INSERT CONFIG
    # Set this value to True if you want to see graphs each time new lines are generated
    display_lines = True

    # INSERT CONFIG
    np.set_printoptions(precision=14, suppress=True)

    # INSERT CONFIG
    # This value can be changed manually over time for experimentation
    alpha = 1

    # FILE_EXISTS FUNCTION WAS DEFINED HERE
    user_input_data, time_amt = file_exists(filename)

    # USER_QUESTION FUNCTION WAS DEFINED HERE
    num_lines, num_segments, num_iterations = user_questions()

    # PUT IN A CLASS
    # Save the current time as a point of reference for determining intervals that change over time
    start_time = datetime.now()

    # CONDITIONS_MET FUNCTION WAS DEFINED HERE
    lines = conditions_met(time_amt, user_input_data,
                           num_lines, num_segments, num_iterations)

    # Check if the user wants to see lines displayed or not
    if display_lines:

        # This is the first set of lines we plot
        print("Plotting Lines ...")
        plot_lines(lines, num_segments)

    # CREATE A FUNCTION HERE UNTIL THE END OF THIS FILE CALLED "start_program"

    # Initially, the previous time is the starting time and the previous segment is None
    prev_time = start_time
    prev_seg = None

    for i in range(1, num_segments + 1):

        # Reset the user input since there's a new point being inputted
        # This value must be zero so that the first subtraction does nothing
        prev_input_1 = 0
        prev_input_2 = 0

        # print("Input " + str(num_segments) + " numbers on a separate line: ")

        # Store the new prev_time and prev_seg from the newly collected segment data from the user
        prev_time, prev_seg = get_segment(start_time, prev_time, prev_seg)

        # Note: total_seconds() converts the time difference to seconds and then we divide by 60 to convert it to mins
        prev_seg_mins = prev_seg.total_seconds() / 60

        # Append the newest time to our set of data we've collected
        user_input_data = np.append(user_input_data, [prev_seg_mins])

        # Get the mean of all user inputted data
        user_mean = user_input_data.mean()

        # Get the standard deviation of all user inputted data
        user_std_dev = user_input_data.std()

        print("Recreating " + str(num_lines) + " lines from the user data...")
        print("New Standard Deviation = " + str(user_std_dev))
        print("New Mean = " + str(user_mean))
        print()

        # print("All of your data since conception: " + str(user_input_data))

        # Train and print the new lines
        # TODO: Uncomment the following line and comment the next line out if you want to use train_lines
        # lines = train_lines(user_mean, user_std_dev, num_lines, dimensions, num_segments, num_iterations)
        lines = train_lines_2(user_mean, user_std_dev,
                              num_lines, num_segments, num_iterations)

        # Check if the user wants to see lines displayed or not
        if display_lines:

            # This is the first set of lines we plot
            print("Plotting Lines ...")
            plot_lines(lines, num_segments)

        ########################
        # AM PM FUNCTION CALL HERE
        x_input = delta_time(start_time, prev_time)
        ########################

        # This contains the total amount of time from the time of conception to the time we finished our last segment.
        # This value will be passed to all lines we generated to determine the correct range of intervals to report.
        # TODO: Uncomment the following line if you want to use more than one dimension (you'll also have to change all
        #       function calls to be train_lines rather than train_lines_2 in order for this to work)
        # curr_x = np.array([x_input ** power for power in range(1, dimensions + 1)])
        curr_x = np.array([x_input])

        # print("curr_x: " + str(curr_x))

        curr_y = np.array([])

        for line in range(len(lines)):

            # Append the resulting y value when plugging curr_x into each respective line
            curr_y = np.append(
                curr_y, lines[line].predict(curr_x.reshape(1, -1)))

        # TODO: Find the function (if any) that is ABOVE the y value of i, the function (if any)
        #       that is BELOW the y value of i - 1 and all functions inbetween i - 1 and i. Report the two functions
        #       that have the fastest completion time and the slowest completion time.
        # Note: If there's only one function that meets the requirements and it's ABOVE, report the interval [one_func, ?]
        #       If there's only one function that meets the requirements and it's BELOW, report the interval [?, one_func]
        #       If there's zero functions that meet the requirements, report [?, ?]

        y_index = 0

        # First, iterate through all curr_y values and remove those that exceed the number of segments or are less than 0
        # (do this by deleting those entries)
        while y_index < len(curr_y):

            if curr_y[y_index] < 0 or curr_y[y_index] > num_segments:

                # print("Before (" + str(y_index) + ") " + str(curr_y))

                # Remove that function from consideration
                curr_y = np.delete(curr_y, y_index, 0)

                # print("After (" + str(y_index) + ") " + str(curr_y))

            else:

                # Increment the index
                y_index += 1

        # print("Removing all lines that aren't in the interval [" + str(i-1) + "," + str(i) + "]")
        # print("Y Values Before: " + str(curr_y))

        indexes, curr_y = remove_out_of_range(curr_y, i - 1, i)

        # print("Y Values After: " + str(curr_y))
        # print("Line Indexes: " + str(indexes))

        # This contains all y values of the remaining lines that cross the line y = num_segments
        end_points = np.array([])

        # Get all lines at the remaining indexes and save their y values when y = num_segments
        for line_index in indexes:

            # Note that we're appending -num_segments because we need to shift each curve down
            # by num_segments to align it with the x-axis so we can find the roots
            coefficients = np.append(
                np.flip(lines[line_index].coef_, 0), -num_segments)

            # Get all roots (including imaginary roots)
            coef_roots = np.roots(coefficients)

            # Get only the real roots and throw away the imaginary roots
            real_coef_roots = np.real(coef_roots[np.isreal(coef_roots)])

            root_index = 0

            while root_index < len(real_coef_roots):

                # If the root is less than zero, we must throw it out because it's irrelevant
                if real_coef_roots[root_index] < 0:

                    real_coef_roots = np.delete(real_coef_roots, root_index, 0)

                else:

                    # Increment the root index
                    root_index += 1

            if real_coef_roots.size > 0:

                # Append the root which has the smallest x value (from the previous while loop, it must be >= 0)
                end_points = np.append(end_points, np.min(real_coef_roots, 0))

        # Make sure we have at least one root
        if end_points.size == 0:

            print("Predicted Interval: [?, ?]")

        else:

            start_time_timestamp = start_time.timestamp()

            min_end_point = np.min(end_points, 0)

            max_end_point = np.max(end_points, 0)

            print("Predicted Interval: [" + str(min_end_point) + "," +
                  str(max_end_point) + "] (cumulative time in minutes)")

            # For these two times we convert the starting time to a timestamp, add in the number of minutes
            # for the line with the fastest end time and convert it back to a datetime object.
            # The same thing happens for the worst case time except we add in the number of minutes for the
            # slowest end time rather than the fastest end time.
            print("Best Case Time: " + str(datetime.fromtimestamp(start_time_timestamp +
                                                                  (60 * min_end_point)).strftime('%Y/%m/%d %I:%M:%S %p')))
            print("Worst Case Time: " + str(datetime.fromtimestamp(start_time_timestamp +
                                                                   (60 * max_end_point)).strftime('%Y/%m/%d %I:%M:%S %p')))

        # Backup the current date we have in a json file
        np.savetxt(filename, user_input_data, delimiter=',')

        # cont = input("Would you like to continue? (Y/N) ")
        print("You have completed: " + str(i) + " / " +
              str(num_segments) + " segments\n\n")

    print("Done!")

    print(os.system("pause"))
