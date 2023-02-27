import numpy as np
from datetime import datetime
import os
from methods import *
import config_files as cf

# TEST
from task import *
schedule = Schedule()
task_info1 = Task_Information("test", "test", 1, 1, 1, 1, True)
task_info1.create_lines()
task_info2 = Task_Information("hello", "test", 1, 1, 1, 1, True)
task_info2.create_lines()
schedule.add_task(task_info1)
schedule.add_task(task_info2)
schedule.to_file()
schedule.print_names()
schedule.from_file()
schedule.remove_task(task_info1)

# TEST


def running_code():
    # INSERT CONFIG
    filename = f"csv_files/{cf.FILE_NAME}"

    # INSERT CONFIG
    # Set this value to True if you want to see graphs each time new lines are generated
    display_lines = cf.DISPLAY_LINES

    # INSERT CONFIG
    np.set_printoptions(precision=14, suppress=True)

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

    # CREATE A FUNCTION HERE UNTIL THE END OF THIS FILE CALLED "start_program"

    # Initially, the previous time is the starting time and the previous segment is None
    prev_time = start_time
    prev_seg = None

    for i in range(1, num_segments + 1):
        # Store the new prev_time and prev_seg from the newly collected segment data from the user
        # prev_time - The clock time when the last segment was completed
        # prev_seg - The time difference between the most current segment that's been completed
        #            and the one prior to that one.
        prev_time, prev_seg = get_segment(start_time, prev_time, prev_seg)

        # Note: total_seconds() converts the time difference to seconds and then we divide by 60 to convert it to mins
        # prev_seg_mins - The number of minutes between the prior and currently completed segment
        prev_seg_mins = prev_seg.total_seconds() / 60

        prev_time_mins = delta_time(start_time, prev_time)

        # Append the newest time to our set of data we've collected
        # user_input_data - The list of segment completion times (originally generated from the CSV)
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
        lines = train_lines_2(user_mean, user_std_dev,
                              num_lines, num_segments,
                              num_iterations, prev_time_mins, i)

        # Check if the user wants to see lines displayed or not
        if display_lines:
            # This is the first set of lines we plot
            print("Plotting Lines ...")
            plot_lines(lines, num_segments, prev_time_mins, i)

        # Get the endpoints for where each line intersects the y = num_segments line

        end_points = retrieve_endpoints(lines, num_segments)

        # REPLACE WITH return_interval() METHOD
        # Make sure we have at least one root
        try:
            start_time_timestamp, min_end_point, max_end_point = return_interval(
                end_points, start_time)

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
        except Exception as e:
            print(e)

        # Backup the current date we have in a csv file
        save_file(filename, user_input_data)

        # cont = input("Would you like to continue? (Y/N) ")
        print("You have completed: " + str(i) + " / " +
              str(num_segments) + " segments\n\n")

    print("Done!")

    print(os.system("pause"))
