import numpy as np
import matplotlib.pyplot as plt
import random as rand
from sklearn import linear_model
from datetime import datetime
import time
import decimal

np.set_printoptions(precision = 14, suppress=True)

# This value can be changed manually over time for experimentation
alpha = 1


def standardize(data):

    if len(data.shape) == 1:

        N = len(data)

    else:

        N = len(data[0])

    for col in range(N - 1):

        # We standardize each column
        data[:, col] = (data[:, col] - data[:, col].mean()) / data[:, col].std()

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

        #print("Dotting " + str(w[index]) + " and " + str(x[index]))

        total += (w[index] * x[index])

    #print("Performing " + str(total) + " - " + str(x[len(x) - 1]))

    # Finally, subtract the Y value
    total -= x[len(x) - 1]

    #print("Getting a result of " + str(total))

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

    #print("NEW W: " + str(w))

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
        time = np.array([0 for _ in range(num_iterations)])

        # total_time contains all x points for all segments generated for the current line
        total_time = np.array([])

        # total_y contains all y points for all segments generated for the current line
        total_y = np.array([])

        # This is how many segments we start at
        segs_done = 1

        for _ in range(num_segments):

            # Update the time values by adding the mean and original time
            time = np.add(time, np.random.normal(mean, std_dev, num_iterations))

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
        lines[line] = regr.fit(total_time.reshape(-1,1), total_y)

    # Return our newly formed lines
    return lines




# Note: The second to last parameter was time_amt, but I removed it because it was never used
# Note: This is the ORIGINAL function we call. Above this function is train_lines_new, which only
#       fits the lines according to the MEAN of each segment
def train_lines(mean, std_dev, num_lines, dimensions, num_segments, num_iterations):

    # Generate 10,000 random numbers from the Gaussian Distribution (with mean 0 and std_dev)
    # TODO: This following line was the initial line that worked, so use it if needed
    # x = np.random.normal(0, std_dev, 10000)
    # x = np.random.normal(mean, std_dev, 10000)


    # # This will define the number of lines we need to make that gradient descent will be performed on
    # num_lines = int(input("How many intervals would you like there to be? "))

    # dimensions = int(input("How many degrees would you like? "))

    # num_segments = int(input("How many segments are there? "))

    # time_amt = int(input("How many time units are there? "))

    # num_iterations = int(input("How many iterations of initial training do you want? "))



    # Note: Lines are of the form y = (w1) * (x1) + (w2) * (x1)^2 ..., so the # of weights = the # dimensions
    #       and the # of arrays of weights = the # of lines
    #lines = np.array([[0 for _ in range(dimensions)] for _ in range(num_lines)])
    lines = [[0 for _ in range(dimensions)] for _ in range(num_lines)]

    # Do one set of sampling per line we have (line_index is the index of the current line)
    for line_index in range(num_lines):

        # This is the data we're going to use for the initial training
        data = np.array([])

        # Start the sampling
        # Note: num_interations is the number of complete samples we plug into the least squares
        # Example: If there are 5 components/parts to be completed, then if num_iterations = 4
        #          then the program will generate 5 * 4 = 20 points of data to be plugged into
        #          least squares. Each sample will iterate through the number of components/parts
        #          for the y-value, effectively generating num_iterations sample completions 
        for _ in range(num_iterations):

            # Reset the x and y plot arrays
            # x_plot = [0]
            # y_plot = [0]

            # This is the current time as we progress towards time_amt
            curr_time = 0

            # This is the number of segments we've completed
            segs_done = 0

            # Sample 1 iteration of the set of segments from the Gaussian Distribution
            # x_sample = np.random.choice(x, num_segments)
            x_sample = np.random.normal(mean, std_dev, num_segments)

            # Check if we've completed all segments and we're not out of time
            for i in range(len(x_sample)):

                # This is a point representing all x values and the y value (the y value is located at the end)
                point = []

                # Try this value as being (# of steps) / 4
                #std_dev = ((time_amt - curr_time) / (num_segments - segs_done)) / 4

                # TODO: Uncomment these two lines of code if commenting them breaks the code! (These two lines appear to break the program)
                # if curr_time > time_amt:

                #     break

                # TODO: Uncomment these two lines, since they're required to make the program work (although you should experiment with them). I only commented these for testing purposes.
                # while curr_time + x_sample[i] + mean < curr_time:

                #     x_sample[i] = np.random.choice(x, 1)

                # Update our time
                #curr_time += x_sample[i] + (std_dev * 4)
                # TODO: The following line was the original line. If you uncomment it, then see the TODO for when we first assigned x and uncomment it as well
                # curr_time += x_sample[i] + mean
                curr_time += x_sample[i]

                # Update the number of segments done
                segs_done += 1

                # Input the x value for the training point
                point.append(curr_time)

                # Iterate through the rest of the dimensions and for each additional dimension add x to that power
                # until all dimensions are filled
                for x_pow in range(2, dimensions + 1):

                    # Append an x value with an increasing power to the new point
                    point.append(curr_time ** x_pow)

                # Finally, append the y value
                point.append(segs_done)

                # Now we copy the new point to data
                
                # Check if the data isn't empty
                if data.size != 0:

                    # Append a new row
                    data = np.vstack([data, point])

                # The data is empty
                else:

                    # Append the point as the first row to data
                    data = np.append(data, point)

                # x_plot.append(curr_time)
                # y_plot.append(segs_done)
        
        #print("LINE: " + str(lines[line_index]))
        #print("DATA: " + str(data))

        #data = standardize(data)

        #print("DATA after standardizing: " + str(data))

        # Train the current line the randomly sampled Gaussian Distribution data
        #lines[line_index] = train_weights(lines[line_index], data)

        # Pass the weights and the x and y data
        lines[line_index] = least_squares(data[:, 0:dimensions], data[:, dimensions])

        # Note: The following line was the original call to the parameter "w" in least_squares, but the parameter isn't used
        # lines[line_index] = least_squares(lines[line_index], data[:, 0:dimensions], data[:, dimensions])


    # print("Lines: ")

    # for line in range(num_lines):

    #     print("y = ", end='')

    #     for num in range(dimensions):

    #         if lines[line][num] >= 0:

    #             print("+", end='')

    #         print(str(lines[line][num]) + "x^" + str(num + 1), end='')

    #     print()
    

    # for line in range(2):

    #     print("y = ", end='')

    #     if line == 0:

    #         if lines[line].intercept_ < 0:

    #             print("-" + str(lines[line].intercept_) + "x ")
            
    #         else:

    #             print(str(lines[line].intercept_) + "x ")

    #     else:

    #         for num in lines[line].coef_:

    #             if num < 0:

    #                 print("-" + str(lines[line].coef_[num]) + "x^" + str(num + 2) + " ")

    #             else:

    #                 print("+" + str(lines[line].coef_[num]) + "x^" + str(num + 2) + " ")


    # Note: Uncomment these lines if you want to print the equation of the line

    # ---------------------------------------------------------------------------------------------------------------

    # for line in range(len(lines)):

    #     print("y = ", end='')

    #     for num_index in range(len(lines[line].coef_)):

    #         if lines[line].coef_[num_index] < 0:

    #             print_without_e(lines[line].coef_[num_index])
    #             print("x^" + str(num_index+1), end='')

    #         else:

    #             print("+", end='')
    #             print_without_e(lines[line].coef_[num_index])
    #             print("x^" + str(num_index+1), end='')

    #     print()

    # ---------------------------------------------------------------------------------------------------------------

        #print(lines[line].coef_)
        #print(lines[line].intercept_)

    # Return the lines
    return lines

# This function takes any float and prints it without scientific notation
def print_without_e(some_float):
    
    #print(some_float)
    
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
def get_segment(start_time, prev_time, prev_seg = None):

    # We start out not having any choice made by the user
    choice = None

    while choice != 'c':

        choice = input("Would you like to see i(nfo) or c(omplete a segment)? i or c? ")

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

            print("\nInitial Starting Time: " + str(start_time.strftime('%Y/%m/%d %I:%M:%S %p')))

            print("Time Since Conception: " + str(conception_time))

            print("Previous Clock Time: " + str(prev_time.strftime('%Y/%m/%d %I:%M:%S %p')))

            if prev_seg != None:
                
                print("Previous Segment Time: " + str(prev_seg))
            
            print("Current Clock Time: " + str(curr_time.strftime('%Y/%m/%d %I:%M:%S %p')))

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
                #i -= 1

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
                #i -= 1

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