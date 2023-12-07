"use strict";

document
  .getElementById("join-multi-form")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const gameCode = document.getElementById("multi-game-code").value;
    const gameOption = document.querySelector(
      'input[name="game-option"]:checked'
    ).value;

    console.log(gameCode);

    if (gameOption === "host") {
      console.log("Hosting game! Share your game code with a friend!");
    } else if (gameOption === "join") {
      console.log("Joining game!");
    }
  });
