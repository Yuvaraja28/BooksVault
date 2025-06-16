// Function to open the modal
function openModal(message, title) {
  // Get the modal
  var modal = document.getElementById("myModal");  
  document.getElementById("modal-message").innerText = message;
  document.getElementById("modal-title").innerText = title;
  modal.style.display = "block";
}

var span = document.getElementsByClassName("close")[0];
// When the user clicks on <span> (x), close the modal
if (span) {
  span.onclick = function() {
    var modal = document.getElementById("myModal");  
    modal.style.display = "none";
  }
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    var modal = document.getElementById("myModal");  
    modal.style.display = "none";
  }
}
