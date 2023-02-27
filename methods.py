import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from datetime import datetime
import os
import decimal


# def file_exists(filename):
#     """ Check if the file exists """

#     if os.path.exists(filename):
#         # Load previous data
#         user_input_data = np.loadtxt(filename, delimiter=',')

#         # There's no need for a time_amt since we've already collected data
#         # time_amt = None

#     else:
#         # Create a new array
#         user_input_data = np.array([])

#         # We haven't collected data yet, so we need the user to guess the first amount of time
#         # time_amt = float(input(
#         #    "Since the dataset is new, how many time units (in minutes) do you expect to complete this task? "))

#     return user_input_data  # , time_amt


def save_file(filename, user_input_data):
    """ Save the data to a file """

    # Save the data to a file
    np.savetxt(filename, user_input_data, delimiter=',')
    print("Data saved to " + filename)


def user_questions():
    """ Ask the user questions about their task """

    # This will define the number of lines we need to make that gradient descent will be performed on
    num_lines = int(input("How many intervals would you like there to be? "))

    # dimensions = int(input("How many degrees would you like? "))
    num_segments = int(input("How many segments are there? "))

    # time_amt = float(input("How many time units are there? "))

    num_iterations = int(
        input("How many iterations of initial training do you want? "))

    return num_lines, num_segments, num_iterations


def retrieve_endpoints(lines, num_segments):
    """ Retrieve the endpoints of the lines """

    end_points = np.array([])

    for line_index in range(len(lines)):

        coefficients = np.append(
            np.flip(lines[line_index].coef_, 0), -num_segments)

        coef_roots = np.roots(coefficients)

        end_points = np.append(end_points, coef_roots)

    return end_points


def return_interval(end_points, start_time):
    """ Return the interval of the end points """

    if end_points.size == 0:

        raise NotImplementedError("Predicted Interval: [?, ?]")

    else:
        start_time_timestamp = start_time.timestamp()
        min_end_point = np.min(end_points)
        max_end_point = np.max(end_points)

    return start_time_timestamp, min_end_point, max_end_point


def conditions_met(time_amt, user_input_data, num_lines, num_segments, num_iterations):
    """ Check if the conditions are met """

    # This condition is only met if we're working off a csv file we already know
    if time_amt == None:

        # This means we should calculate the mean of our already existing dataset when training our first lines
        user_mean = user_input_data.mean()
        user_std_dev = user_input_data.std()

        print("Starting Standard Deviation = " + str(user_std_dev))
        print("Starting Mean = " + str(user_mean))

        lines = train_lines_2(user_mean, user_std_dev,
                              num_lines, num_segments, num_iterations)

    # Meaning that the dataset is new
    else:

        # Train the lines initially, which means we have to guess the first mean by using the time_amt variable
        # provided by the user to calculate an estimated mean. Note that we assume the standard deviation is 1 here
        # as that is the default case. We don't need to prompt the user for this, because there's no way the user
        # could accurately predict this value. Especially considering this program's job is basically to find this value.
        # Note: We could also generate a random number or 0 as a default for the mean, but its better to have an accurate guess
        #       than to start off with a number that is completely off
        lines = train_lines_2(time_amt / num_segments, 1,
                              num_lines, num_segments, num_iterations)

    return lines


def delta_time(start_time, prev_time):
    """ Get the time difference between the start time and the previous time """

    if (start_time - prev_time).total_seconds() >= 0:

        # Get the time from inception in terms of minutes
        x_input = (start_time - prev_time).total_seconds() / 60

    else:

        # Get the time from inception in terms of minutes
        x_input = (prev_time - start_time).total_seconds() / 60

    return x_input


def standardize(data):
    """ Standardize the data """

    if len(data.shape) == 1:

        N = len(data)

    else:

        N = len(data[0])

    for col in range(N - 1):

        # We standardize each column
        data[:, col] = (data[:, col] - data[:, col].mean()) / \
            data[:, col].std()

    return data


def least_squares(x, y):
    """ Perform least squares on the data """

    regr = linear_model.LinearRegression(fit_intercept=True)
    regr.fit(x, y)

    return regr


def plot_lines(lines, max_y, elapsed_x_time=0, curr_y_seg=0):
    """ Plot the lines """

    # This function plots the newly formed lines after performing least squares upon the
    # completion of each segment.

    # Note: This function assumes each function is linear, so x^2, x^3 ... won't work

    # lines: a list of numpy lines
    # max_y: num_segments; the maximum y value
    # x_values: the x value of the intersection between the line y = max_y and each line

    x_values = np.array([])

    # Get all lines at the remaining indexes and save their y values when y = num_segments
    for line_index in range(len(lines)):

        # Note that we're appending -num_segments because we need to shift each curve down
        # by num_segments to align it with the x-axis so we can find the roots
        coefficients = np.append(np.flip(lines[line_index].coef_, 0), -max_y)

        # Get all roots (including imaginary roots, except in this particular function there are no imaginary roots)
        coef_roots = np.roots(coefficients)

        # Append the root of the current line
        x_values = np.append(x_values, coef_roots)

    # Check if the lengths of the two arrays are the same
    if len(x_values) != len(lines):
        print("Error!")
        print("Length of x_values: " + str(len(x_values)))
        print("Length of lines: " + str(len(lines)))

        exit(1)

    # Get the maximum x value to determine the x bound for the window
    max_x = np.max(x_values)

    # Extract each line in the list of lines
    for line_index in range(len(lines)):

        # Note: We have two values here (our current x position in time and the x-value of where
        #       the line intersects num_segments) because we need two x points (and two y points)
        #       in order to plot a line.
        x = np.array([0, x_values[line_index]])

        # Plot the line
        plt.plot(x, lines[line_index].predict(x.reshape(-1, 1)))

    # Set the upper y and x bounds
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)
    plt.grid()
    plt.plot(elapsed_x_time, curr_y_seg, marker="o",
             markersize=15, markeredgecolor="blue", markerfacecolor="orange")

    # Show the plot
    plt.show()


def summation(w, x, i):
    """ Perform the summation function """

    # This function takes two arrays: w (for the weights) and x (for the input you plug in)
    # and returns the y-predict value upon plugging it into y^ = (w1) * (x1) + (w2) * (x1)^2 ...
    # i is the value of the index from xij (see gradient descent formula)

    # Make sure the dimensions match (we have to add 1 to len(w) because of y)
    if len(w) + 1 != len(x):

        return None

    # Create a total for the dot product and overall summation
    total = 0

    for index in range(len(w)):

        # print("Dotting " + str(w[index]) + " and " + str(x[index]))

        total += (w[index] * x[index])

    # Finally, subtract the Y value
    total -= x[len(x) - 1]

    # Multiply by xij
    total *= x[i]

    return total


def train_weights(w, data):
    """ Perform gradient descent on the weights """

    # This function takes an array of weights, a 2D array of training data and returns new weights
    # after performing gradient descent on each set of weights

    # data.shape returns the length and width of the data array
    if len(data.shape) == 1:

        # This represents the number of examples of data if there's only one example present
        N = 1

    else:

        # This represents the number of examples of data if there's more than one example present
        N = len(data)

    # Iterate through each weight one at a time
    for weight in range(len(w)):

        total_sum = 0

        # Select one entry of data at a time (avoiding the last position since it's the value of Y)
        for data_point in data:

            total_sum += summation(w, data_point, weight)

        # Update each weight
        w[weight] = w[weight] - ((alpha / N) * total_sum)

    # Return the weights
    return w


def train_lines_2(mean, std_dev, num_lines, num_segments, num_iterations, elapsed_x_time=0, curr_y_seg=0):
    """ Train the lines """

    # This is the new and improved version of train_lines. It has several improvements:
    # 1) It relies more heavily on numpy, which drastically improves speed (see plot_testing.py)
    # 2) At each segment (subtask), every separate iteration is condensed into the mean of that
    #    particular distribution. This means that when least squares is plotted it won't be as
    #    affected by the outliers of the distribution and instead focuses solely on the changing
    #    mean value as time progresses, which generates a much better prediction at the end.
    # 3) It doesn't use "dimensions", so in other words it only supports lines rather than non-linear equations

    # Generate the lines by initializing them to zero
    lines = [None for _ in range(num_lines)]

    # Iterate through all lines
    for line in range(num_lines):

        # This is the array containing the mean of the current time at each segment's distribution
        # This allows us to calculate each iteration in parallel, which drastically speeds up the calculation
        time = np.array([0 for _ in range(num_iterations)])

        # total_time contains all x points for all segments generated for the current line
        total_time = np.array([])

        # total_y contains all y points for all segments generated for the current line
        total_y = np.array([])

        # This is how many segments we start at
        for segs_done in range(1, num_segments + 1):

            # Update the time values by adding the mean and original time
            time = np.add(time, np.random.normal(
                mean, std_dev, num_iterations))

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
        lines[line] = regr.fit(total_time.reshape(-1, 1), total_y)

        # The following line of code takes our current position in time and uses the slope
        # that was generated by fit() above to construct each line centered at our current
        # position. In other words, the following line of code is the solution to finding the
        # y intercept when you know the slope and a point.
        lines[line].intercept_ = curr_y_seg - \
            (lines[line].coef_ * elapsed_x_time)
        # print("Y Intercept: " + str(lines[line].intercept_))
        # print("Slope: " + str(lines[line].coef_))

    # Return our newly formed lines
    return lines


def print_without_e(some_float):
    """ Print a float without scientific notation"""

    # Get the string version of our decimal
    str_decimal = decimal.Decimal(str(some_float))

    # Get the number of decimal digits to the right of the decimal point
    decimal_count = abs(str_decimal.as_tuple().exponent)

    # Get the format string for printing
    format_str = '{0:.' + str(decimal_count) + 'f}'

    # Print some_float formatted to the custom number of digits to the
    # right of the decimal point so it prints correctly
    print(format_str.format(some_float), end='')


# REMOVE CHOICE WHEN IMPLEMENTING GUI
def get_segment(start_time, prev_time, prev_seg=None):
    """ Get the current segment """

    # This only gets the user's input from one segment and returns it
    # It will, given the input 'i', display timing information
    # Given the input 'c', this function returns the curr_seg

    # We start out not having any choice made by the user
    choice = None

    while choice != 'c':

        choice = input(
            "Would you like to see i(nfo) or c(omplete a segment)? i or c? ")

        # Get the current time
        curr_time = datetime.now()

        # Make sure that the previous time isn't AM while the old time is PM (from midnight to morning hours)
        if ((prev_time - curr_time).total_seconds() >= 0):

            curr_seg = prev_time - curr_time

        # Display all metrics including:
        # Previous Segment, Previous Time, Current Segment and Current Time
        # This is the case when its PM to AM
        else:
            curr_seg = curr_time - prev_time

        if choice == 'i':

            if ((start_time - curr_time).total_seconds() >= 0):

                # Conception time is the time that has elapsed
                conception_time = start_time - curr_time

            else:

                conception_time = curr_time - start_time

            print("\nInitial Starting Time: " +
                  str(start_time.strftime('%Y/%m/%d %I:%M:%S %p')))

            print("Time Since Conception: " + str(conception_time))

            print("Previous Clock Time: " +
                  str(prev_time.strftime('%Y/%m/%d %I:%M:%S %p')))

            if prev_seg != None:

                print("Previous Segment Time: " + str(prev_seg))

            print("Current Clock Time: " +
                  str(curr_time.strftime('%Y/%m/%d %I:%M:%S %p')))

            print("Current Segment Time: " + str(curr_seg))

            print()

        # This means we need to save the current time difference between the previous clock and current clock
        elif choice == 'c':
            return curr_time, curr_seg
