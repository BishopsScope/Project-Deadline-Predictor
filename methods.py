import numpy as np
import matplotlib.pyplot as plt
import random as rand
from sklearn import linear_model
from datetime import datetime
import time
import os
import decimal

# Check if the file exists


def file_exists(filename):
    if os.path.exists(filename):
        # Load previous data
        user_input_data = np.loadtxt(filename, delimiter=',')

        # There's no need for a time_amt since we've already collected data
        time_amt = None

    else:
        # Create a new array
        user_input_data = np.array([])

        # We haven't collected data yet, so we need the user to guess the first amount of time
        time_amt = float(input(
            "Since the dataset is new, how many time units (in minutes) do you expect to complete this task? "))

    return user_input_data, time_amt


def user_questions():
    # This will define the number of lines we need to make that gradient descent will be performed on
    num_lines = int(input("How many intervals would you like there to be? "))

    # dimensions = int(input("How many degrees would you like? "))

    num_segments = int(input("How many segments are there? "))

    # time_amt = float(input("How many time units are there? "))

    num_iterations = int(
        input("How many iterations of initial training do you want? "))

    return num_lines, num_segments, num_iterations


def conditions_met(time_amt, user_input_data, num_lines, num_segments, num_iterations):
    # This condition is only met if we're working off a csv file we already know
    if time_amt == None:

        # This means we should calculate the mean of our already existing dataset when training our first lines
        user_mean = user_input_data.mean()
        user_std_dev = user_input_data.std()

        print("Starting Standard Deviation = " + str(user_std_dev))
        print("Starting Mean = " + str(user_mean))

        # TODO: Uncomment the following line and comment the next line out if you want to use train_lines
        # lines = train_lines(user_mean, user_std_dev, num_lines, dimensions, num_segments, num_iterations)
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
        # TODO: Uncomment the following line and comment the next line out if you want to use train_lines
        # lines = train_lines(time_amt / num_segments, 1, num_lines, dimensions, num_segments, num_iterations)
        lines = train_lines_2(time_amt / num_segments, 1,
                              num_lines, num_segments, num_iterations)

    return lines

# Check to make sure changes in PM to AM don't change the sign/value of the time difference


def delta_time(start_time, prev_time):

    if (start_time - prev_time).total_seconds() >= 0:

        # Get the time from inception in terms of minutes
        x_input = (start_time - prev_time).total_seconds() / 60

    else:

        # Get the time from inception in terms of minutes
        x_input = (prev_time - start_time).total_seconds() / 60

    return x_input


def standardize(data):
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

    regr = linear_model.LinearRegression(fit_intercept=False)
    regr.fit(x, y)

    return regr


# This function plots the newly formed lines after performing least squares upon the
# completion of each segment.
#
# Note: This function assumes each function is linear, so x^2, x^3 ... won't work
#
# lines: a list of numpy lines
# max_y: num_segments; the maximum y value
# x_values: the x value of the intersection between the line y = max_y and each line
def plot_lines(lines, max_y):

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

    if len(x_values) != len(lines):

        print("Error!")
        print("Length of x_values: " + str(len(x_values)))
        print("Length of lines: " + str(len(lines)))

        exit(1)

    # Get the maximum x value to determine the x bound for the window
    max_x = np.max(x_values, 0)

    # Extract each line in the list of lines
    for line_index in range(len(lines)):

        x = np.array([0, x_values[line_index]])

        # Plot the line
        plt.plot(x, lines[line_index].predict(x.reshape(-1, 1)))

    # Set the upper y and x bounds
    plt.xlim(0, max_x)
    plt.ylim(0, max_y)

    # Show the plot
    plt.show()


# This function takes two arrays: w (for the weights) and x (for the input you plug in)
# and returns the y-predict value upon plugging it into y^ = (w1) * (x1) + (w2) * (x1)^2 ...
# i is the value of the index from xij (see gradient descent formula)
def summation(w, x, i):

    # Make sure the dimensions match (we have to add 1 to len(w) because of y)
    if len(w) + 1 != len(x):

        return None

    # Create a total for the dot product and overall summation
    total = 0

    for index in range(len(w)):

        # print("Dotting " + str(w[index]) + " and " + str(x[index]))

        total += (w[index] * x[index])

    # print("Performing " + str(total) + " - " + str(x[len(x) - 1]))

    # Finally, subtract the Y value
    total -= x[len(x) - 1]

    # print("Getting a result of " + str(total))

    # print("Multiplying the " + str(i) + " column x value to total")

    # print("Multiplying " + str(total) + " by " + str(x[i]))

    # Multiply by xij
    total *= x[i]

    # print("Finally getting a result of " + str(total))

    # print("Current total: " + str(total))

    return total


# This function takes an array of weights, a 2D array of training data and returns new weights
# after performing gradient descent on each set of weights
def train_weights(w, data):

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

            # print("W (" + str(weight) + "): " + str(w[weight]))

            # Now we execute the gradient descent formula:
            # wj = wj - (alpha / N) * (Summation((y^ - y) * xij))

            # w[line_index][weight] = w[line_index][weight] - ((alpha / len(data)) * )

            # print("Old Total Sum: " + str(total_sum))

            total_sum += summation(w, data_point, weight)

            # print("New Total Sum: " + str(total_sum))

        # print("Final total " + str(weight) + " is " + str(total_sum))

        # print("Updating the new weight with: " + str(w[weight]) + " - (" + str(alpha) + " / " + str(N) + ") * " + str(total_sum))
        # print("Simplifying to: " + str(w[weight]) + " - (" + str(alpha / N) + ") * " + str(total_sum))
        # print("Simplifying to: " + str(w[weight]) + " - " + str((alpha / N) * total_sum))
        # print("Giving a value of: " + str(w[weight] - ((alpha / N) * total_sum)))

        # Update each weight
        w[weight] = w[weight] - ((alpha / N) * total_sum)

        # print("New weight value: " + str(w[weight]))

    # print("NEW W: " + str(w))

    # Return the weights
    return w

# This is the new and improved version of train_lines. It has several improvements:
# 1) It relies more heavily on numpy, which drastically improves speed (see plot_testing.py)
# 2) At each segment (subtask), every separate iteration is condensed into the mean of that
#    particular distribution. This means that when least squares is plotted it won't be as
#    affected by the outliers of the distribution and instead focuses solely on the changing
#    mean value as time progresses, which generates a much better prediction at the end.
# 3) It doesn't use "dimensions", so in other words it only supports lines rather than non-linear equations


def train_lines_2(mean, std_dev, num_lines, num_segments, num_iterations):

    # Generate the lines by initializing them to zero
    lines = [None for _ in range(num_lines)]

    # Iterate through all lines
    for line in range(num_lines):

        # This is the array containing the mean of the current time at each segment's distribution
        # This allows us to calculate each iteration in parallel, which drastically speeds up the calculation
        # TODO: Replace 0 (the starting x point when simulating) with the current time (pass the current time
        #       as an x-value to train_lines_2())
        time = np.array([0 for _ in range(num_iterations)])

        # total_time contains all x points for all segments generated for the current line
        total_time = np.array([])

        # total_y contains all y points for all segments generated for the current line
        total_y = np.array([])

        # This is how many segments we start at
        # TODO: Replace segs_done = 1 with the segment we are currently on.
        segs_done = 1

        for _ in range(num_segments):

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

            # Update this since we just completed a segment
            segs_done += 1

        # Fit the line and save it in our list of lines
        regr = linear_model.LinearRegression(fit_intercept=False)
        lines[line] = regr.fit(total_time.reshape(-1, 1), total_y)

    # Return our newly formed lines
    return lines


def print_without_e(some_float):

    # print(some_float)

    # Get the string version of our decimal
    str_decimal = decimal.Decimal(str(some_float))

    # Get the number of decimal digits to the right of the decimal point
    decimal_count = abs(str_decimal.as_tuple().exponent)

    # Get the format string for printing
    format_str = '{0:.' + str(decimal_count) + 'f}'

    # Print some_float formatted to the custom number of digits to the
    # right of the decimal point so it prints correctly
    print(format_str.format(some_float), end='')


# This only gets the user's input from one segment and returns it
# It will, given the input 'i', display timing information
# Given the input 'c', this function returns the curr_seg
def get_segment(start_time, prev_time, prev_seg=None):

    # We start out not having any choice made by the user
    choice = None

    while choice != 'c':

        choice = input(
            "Would you like to see i(nfo) or c(omplete a segment)? i or c? ")

        # Display all metrics including:
        # Previous Segment, Previous Time, Current Segment and Current Time
        if choice == 'i':

            # Get the current time
            curr_time = datetime.now()

            # Make sure that the previous time isn't AM while the old time is PM (from midnight to morning hours)
            if ((prev_time - curr_time).total_seconds() >= 0):

                curr_seg = prev_time - curr_time

            # This is the case when its PM to AM
            else:

                curr_seg = curr_time - prev_time

            if ((start_time - curr_time).total_seconds() >= 0):

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

            # Get the current time
            curr_time = datetime.now()

            # Make sure that the previous time isn't AM while the old time is PM (from midnight to morning hours)
            if ((prev_time - curr_time).total_seconds() >= 0):

                curr_seg = prev_time - curr_time

            # This is the case when its PM to AM
            else:

                curr_seg = curr_time - prev_time

            # Return the current segment time and the current clock time (which will be used as the prev_time next round)
            return curr_time, curr_seg

# Remove all values in arr less than val


def remove_out_of_range(arr, lower_bound, upper_bound):

    # We need a list of all indexes, because we want to return the indexes of the lines that are within range
    # rather than their y-value which is unidentifiable
    index_list = np.array([i for i in range(len(arr))])

    # Get the array of values related to the lower bound
    lower_arr = lower_bound - arr

    # This is the starting value, but this should never be negative
    min_index = 0

    # Make sure min_index doesn't start on a negative value, since that wouldn't make sense
    while min_index < len(lower_arr) and lower_arr[min_index] < 0:

        min_index += 1

    i = min_index + 1

    while i < len(lower_arr):

        # Only check if the current value is >= 0
        if lower_arr[i] >= 0:

            # if min_index < 0:

            #     min_index = i

            if lower_arr[min_index] > lower_arr[i]:

                # Remove the previous element, since it's no longer the closest value to our lower bound
                lower_arr = np.delete(lower_arr, min_index, 0)
                arr = np.delete(arr, min_index, 0)
                index_list = np.delete(index_list, min_index, 0)
                # i -= 1

                # This is now the closest value to our lower bound
                min_index = i - 1

            else:

                # Remove our current element, since the value at min_index is closer to the lower bound
                lower_arr = np.delete(lower_arr, i, 0)
                arr = np.delete(arr, i, 0)
                index_list = np.delete(index_list, i, 0)

                # Note: We don't need to subtract 1 from i in this case, because we're deleting the value that were at

        else:

            i += 1

    # arr has changed, so just subtract upper_bound from the array to get the upper_arr.
    # This saves time, because we don't have to go through elements that were already deleted
    upper_arr = arr - upper_bound

    max_index = 0

    # Make sure min_index doesn't start on a negative value, since that wouldn't make sense
    while max_index < len(upper_arr) and upper_arr[max_index] < 0:

        max_index += 1

    i = max_index + 1

    while i < len(upper_arr):

        # Only check if the current value is >= 0
        if upper_arr[i] >= 0:

            if upper_arr[max_index] > upper_arr[i]:

                # We must check to see if deleting the value at max_index changes min_index
                # Note: Maintaining the min_index isn't important for what we're doing, which is why
                #       I commented this out
                # if max_index < min_index:

                #     min_index -= 1

                # Remove the previous element, since it's no longer the closest value to our upper bound
                upper_arr = np.delete(upper_arr, max_index, 0)
                arr = np.delete(arr, max_index, 0)
                index_list = np.delete(index_list, max_index, 0)
                # i -= 1

                # This is now the closest value to our upper bound
                max_index = i - 1

            else:

                # This uses the same reasoning as the above "if" block
                # if i < min_index:

                #     min_index -= 1

                # Remove our current element, since the value at min_index is closer to the upper bound
                upper_arr = np.delete(upper_arr, i, 0)
                arr = np.delete(arr, i, 0)
                index_list = np.delete(index_list, i, 0)

        else:

            i += 1

    return index_list, arr
