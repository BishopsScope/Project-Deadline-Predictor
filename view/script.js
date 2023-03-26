// Onclick of the button'
// window.addEventListener("resize", function(){
//   window.resizeTo(500, 500);
// });

// function prevent_resize() {
//   var width = window.innerWidth;
//   var height = window.innerHeight;
//   if (width < 500) {
//     window.resizeTo(500, height);
//   }
//   if (height < 500) {
//     window.resizeTo(width, 500);
//   }
// }
// window.addEventListener("resize", prevent_resize);
updateTaskList();

function startTaskTest(taskName) {
  // Remove console.log
  console.log("Start Task: " + taskName);
  eel.start_task(taskName)
}

function deleteTaskTest(taskName) {
  // Remove console.log
  console.log("Delete Task: " + taskName);
  eel.delete_task(taskName)
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
      var startTask = document.createElement("button");
      startTask.innerHTML = "Start";
      startTask.classList.add("startTask");
      // Once clicked, we have a test function the does a console log of the name
      startTask.onclick = function() {
        startTaskTest(ret[i]);
      };

      var deleteTask = document.createElement("button");
      deleteTask.innerHTML = "Delete";
      deleteTask.classList.add("deleteTask");
      // Once clicked, we have a test function the does a console log of the name
      deleteTask.onclick = function() {
        deleteTaskTest(ret[i]);
      };

      li.appendChild(startTask);
      li.appendChild(deleteTask);
      
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

function create_task() {
  // Naming: category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50
  var category = document.getElementById("category").value;
  var task_name = document.getElementById("taskname").value;
  var segment_number = document.getElementById("segments").value;
  // The checked will return either true or false.
  var display_plot = document.getElementById("displayplot").checked;
  var num_lines = document.getElementById("numline").value;
  var iterations = document.getElementById("iterations").value;

  if (correctInput()) {
    eel.create_task(category, task_name, segment_number, display_plot, num_lines, iterations)
    updateTaskList();
  }  
}

