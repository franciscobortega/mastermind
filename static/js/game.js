"use strict";

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("guess-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      // Extract the user's guess and secret code from the form
      let guessInput = document.getElementById("guess-input").value;
      let secretCode = document.getElementById("secret-code").value; // Consider changing this to server-side variable

      let formData = new FormData();

      // Append the user's guess and secret code to the form data
      formData.append("guess", guessInput);
      formData.append("secret_code", secretCode);

      // Send the data to the server
      fetch("/guess", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Update UI with feedback from guess
          displayFeedback(guessInput, data.feedback);
        })
        .catch((error) => {
          console.error("Error:", error);
        });

      // Clear the form
      document.getElementById("guess-form").reset();
    });

  function displayFeedback(guess, feedback) {
    // Create a new list item element for the feedback history
    const guessesContainer = document.querySelector(".guesses-container");

    const guessElement = document.createElement("li");
    guessElement.textContent = guess;

    guessesContainer.appendChild(guessElement);

    // Append the new list item to the feedback container

    const feedbackContainer = document.querySelector(".feedback-container");

    const feedbackElement = document.createElement("li");
    feedbackElement.textContent = feedback;

    feedbackContainer.appendChild(feedbackElement);
  }
});
