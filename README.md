# Project-Deadline-Predictor

## Members:

Anthony Maida amaida@csu.fullerton.edu

Steven Burroughs bishopsscope@csu.fullerton.edu

## Purpose:

The purpose of this project is to create a program to manage your time. You put in a task that you would like to keep track of and divide into segments. The application will keep track of how long it takes for a user to complete a task and then use it to continuously determine how long it takes to complete the task.

## Prerequisites

You will need to have Python 3.6 or later and pip installed on your computer.

## How to use run it:

1. The first step is to ensure you have python3 and pip installed.

2. After that, unzip the source code files. Assuming you’re running your code on Linux, open up a terminal and type “python3 -m venv env” to create a virtual environment. If you’re using a different operating system, read https://docs.python.org/3/library/venv.html to create a virtual environment for your platform. Next, type “source env/bin/activate”, or if you’re on a different operating system follow according to the link above.

3. Run “pip3 install -r requirements.txt”, which will install all the required libraries in your python environment.

4. After that, type in the terminal and run “python3 main.py” and this will launch the Deadline Predictor application. When the application is launched it will create a directory called “TimeManager” in your user home for storing .csv and .pckl. These files hold the information for your schedule and for each category.

## Usage:

1. Create a new task by filling in the information and click "Submit". The newly created task will be displayed in the task section.

2. To start a task, click the green "Start" button next to the task you would like to start. It will redirect to a new page.

3. On the new page, you will be prompted to click the blue "Start" button to get the current time and either resume or being your segment.

4. Once a segment is complete, click the green "Next Segment" button which will track how long it took to complete the segment and calculate how long it will take to complete the task.

5. Once you complete a task or want to go back to the main menu, click the red "Back" button to go back to the main menu.

6. If a user would like to delete a task they created, clicking the red "Delete" button next to a task will remove it from the schedule.

7. Exiting the program is done by clicking on the "X" on the top right of the window.
