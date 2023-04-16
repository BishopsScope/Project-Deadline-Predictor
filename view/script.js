window.addEventListener("DOMContentLoaded", function() {
  // Check if the current page is index.html
  if (window.location.pathname.endsWith("index.html") || window.location.pathname === "/") {
    updateTaskList();
  }
  if (window.location.pathname.endsWith("task.html") || window.location.pathname === "/") {
    displayTaskInfo();
  }
});


function startTask() {
  var taskName = localStorage.getItem("taskName");
  document.getElementById("myUl").innerHTML = "Click Next Segment once a segment is completed.";
  // console.log(taskName)
  // TODO: Move this out of start and put it somewhere else
  //       so that the time isn't restarted every time the
  //       user resumes a task
  eel.setup_computation(taskName);
  var startButton = document.getElementById("start");
  startButton.disabled = true;
  eel.reset_time();
  var nextButton = document.createElement("button");
  nextButton.innerHTML = "Next Segment";
  nextButton.classList.add("nextButton");

  nextButton.onclick = function() {
    eel.next_segment()(function(ret) {

      eel.check_last_computation()(function(ret){
        if (ret)
        {
          nextButton.innerHTML = "Complete Task";
        }
        else
        {
          nextButton.innerHTML = "Next Segment";
        }
      });

      document.getElementById("myUl").innerHTML = "";
      Object.entries(ret).forEach(([key, value]) => {
        const keyElement = document.createElement("span");
        keyElement.className = "key";
        keyElement.textContent = key;

        const valueElement = document.createElement("span");
        valueElement.textContent = value;

        const li = document.createElement("li");
        li.appendChild(keyElement);
        li.appendChild(valueElement);

        document.getElementById("myUl").appendChild(li);
      });
      
      if (Object.keys(ret).length == 0)
      {
        document.getElementById("myUl").innerHTML = "Task has been completed.";
        nextButton.disabled = true;
      }
    });
    eel.update_pickle();
  };
  document.getElementById("nextButton").appendChild(nextButton);
}

function displayTaskInfo() {
  var taskName = localStorage.getItem("taskName");
  // console.log(taskName)
  document.getElementById("task-name").innerHTML = "Task: " + taskName;
  // eel.task_info(taskName)(function(ret) {
  //   document.getElementById("task-info").innerHTML = ret;
  // })
  // if (taskName) {
  //     document.getElementById("task-name").innerHTML = taskName;
  // }
}

function taskScreen(taskName) {
  // window.location.href = "task.html";
  localStorage.setItem("taskName", taskName);
  window.location.href = "task.html";
  // displayTaskName();
}

function createTaskScreen() {
  window.location.href = "index.html";
}

function deleteTask(taskName) {
  // Remove console.log
  console.log("Delete Task: " + taskName);
  eel.delete_task(taskName);
  updateTaskList();
}

function updateTaskList() {
  eel.get_tasks()(function(ret) {
    // Clear previous elements before displaying the tasks again
    document.getElementById("myUl").innerHTML = "";

    // Display the tasks to the screen
    for (let i = 0; i < ret.length; i++) {
      var li = document.createElement("li");
      // ret[i] is the task name
      var text = document.createTextNode(ret[i]);
      li.appendChild(text);

      // Create the start and delete buttons
      var startButton = document.createElement("button");
      startButton.innerHTML = "Start";
      startButton.classList.add("startButton");
      // Once clicked, we have a test function the does a console log of the name
      startButton.onclick = function() {
        // startTask(ret[i]);
        taskScreen(ret[i]);
      };

      var deleteButton = document.createElement("button");
      deleteButton.innerHTML = "Delete";
      deleteButton.classList.add("deleteButton");
      // Once clicked, we have a test function the does a console log of the name
      deleteButton.onclick = function() {
        deleteTask(ret[i]);
      };

      li.appendChild(startButton);
      li.appendChild(deleteButton);
      
      document.getElementById("myUl").appendChild(li);
    }
  })
}

function correctInput() {
  var inputIds = ["category", "taskname", "segments", "numline", "iterations"];
  var validInput = true;

  inputIds.forEach(function (id) {
    var inputElement = document.getElementById(id);
    // Ensure valid values are inputed and that the fields are filled
    if (!inputElement.checkValidity() || inputElement.value.trim() === "") {
      validInput = false;
    }
  });

  return validInput;
}

function createTask() {
  // Naming: category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50
  var category = document.getElementById("category").value;
  var task_name = document.getElementById("taskname").value;
  var segment_number = document.getElementById("segments").value;
  // The checked will return either true or false.
  var display_plot = document.getElementById("displayplot").checked;
  var num_lines = document.getElementById("numline").value;
  var iterations = document.getElementById("iterations").value;

  if (correctInput()) {
    eel.create_task(category, task_name, segment_number, display_plot, num_lines, iterations);
    updateTaskList();
  }  
}