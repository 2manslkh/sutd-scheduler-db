var expanded = false;

function showScheduleFilter() {
  var checkboxes = document.getElementById("schedule-filters");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}

function selectAll(source){
    checkboxes = document.getElementsByName('schedule-filter');

}
