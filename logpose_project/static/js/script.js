
function filterDropdown() {
  var input, filter, ul, li, a, i;
  var maxVisible = 10;
  var visibleCount = 0;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  span = div.getElementsByTagName("span");
  for (i = 0; i < span.length; i++) {
    txtValue = span[i].textContent || span[i].innerText;
    if ((txtValue.toUpperCase().indexOf(filter) > -1) && (visibleCount < maxVisible)) {
      span[i].style.display = "";
      visibleCount++;
    } else {
      span[i].style.display = "none";
    }
  }
} 

function setInput(element) {
    document.getElementById("myInput").value = element.textContent;
}

document.addEventListener("DOMContentLoaded", function() {
    filterDropdown(); // hide items initially beyond maxVisible
});
