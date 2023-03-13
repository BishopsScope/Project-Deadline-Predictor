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

function create_task() {
  // Naming: category, name, num_segments, display_lines=False, num_lines=15, num_iterations=50
  var category = document.getElementById("category").value;
  var task_name = document.getElementById("taskname").value;
  var segment_number = document.getElementById("segments").value;
  var display_plot = document.getElementById("displayplot").value;
  var num_lines = document.getElementById("numline").value;
  var iterations = document.getElementById("iterations").value;
  // eel.test(task_name, segment_number, category)(function(ret) {
  //   document.getElementById("taskname_dis").innerHTML = ret[0];
  //   document.getElementById("segment_dis").innerHTML = ret[1];
  //   document.getElementById("cate_dis").innerHTML = ret[2];
  // });
  eel.create_task(category, task_name, segment_number, display_plot, num_lines, iterations)

  eel.get_tasks()(function(ret) {
    // Clear previous elements before displaying the tasks again
    document.getElementById("myUl").innerHTML = "";

    // Display the tasks to the screen
    for (var i = 0; i < ret.length; i++) {
      var li = document.createElement("li");
      var text = document.createTextNode(ret[i]);
      li.appendChild(text);
      document.getElementById("myUl").appendChild(li);
    }
  })
}
// How to make an app with eel and elect


// function organize_tasks()