// Onclick of the button'
// window.addEventListener("resize", function(){
//   window.resizeTo(500, 500);
// });

function prevent_resize() {
  var width = window.innerWidth;
  var height = window.innerHeight;
  if (width < 500) {
    window.resizeTo(500, height);
  }
  if (height < 500) {
    window.resizeTo(width, 500);
  }
}
window.addEventListener("resize", prevent_resize);

function display_number() {
  var task_name = document.getElementById("taskname").value;
  var segment_number = document.getElementById("segments").value;
  var category = document.getElementById("category").value;
  eel.test(task_name, segment_number, category)(function(ret) {
    document.getElementById("taskname_dis").innerHTML = ret[0];
    document.getElementById("segment_dis").innerHTML = ret[1];
    document.getElementById("cate_dis").innerHTML = ret[2];
  });
}
// How to make an app with eel and elect


