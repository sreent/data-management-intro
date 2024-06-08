// scripts.js

// Function to handle the return to main page action
function returnToMainPage() {
  window.location.href = '/';
}

// Add event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Attach an event listener to the 'Return to Main Page' button if it exists
  var returnButton = document.querySelector('.return-button');
  if (returnButton) {
    returnButton.addEventListener('click', returnToMainPage);
  }

  // Additional event listeners can be added here
  // ...
});
