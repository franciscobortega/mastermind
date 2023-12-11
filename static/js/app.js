"use strict";

// document
//   .getElementById("join-multi-form")
//   .addEventListener("submit", function (e) {
//     e.preventDefault();

//     const gameCode = document.getElementById("multi-game-code").value;
//     const gameOption = document.querySelector(
//       'input[name="game-option"]:checked'
//     ).value;

//     console.log(gameCode);

//     // Send a POST request to the server
//     fetch("/load_lobby", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ gameCode }), // send game code as JSON
//     })
//       .then((response) => {
//         if (response.ok) {
//           // Redirect to the lobby page
//           window.location.href = "/lobby";
//           console.log("You are in the lobby!");
//         } else {
//           console.error("Error:", response.statusText);
//         }
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//       });

//     if (gameOption === "host") {
//       console.log("Hosting game! Share your game code with a friend!");
//     } else if (gameOption === "join") {
//       console.log("Joining game!");
//     }
//   });

// document
//   .getElementById("join-battle-form")
//   .addEventListener("submit", function (e) {
//     e.preventDefault();

//     const gameCode = "ABCD";

//     console.log(gameCode);

//     // Send a POST request to the server
//     fetch("/load_lobby", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ gameCode }), // send game code as JSON
//     })
//       .then((response) => {
//         if (response.ok) {
//           // Redirect to the lobby page
//           window.location.href = "/lobby";
//           console.log("You are in the lobby!");
//         } else {
//           console.error("Error:", response.statusText);
//         }
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//       });

//     if (gameOption === "host") {
//       console.log("Hosting game! Share your game code with a friend!");
//     } else if (gameOption === "join") {
//       console.log("Joining game!");
//     }
//   });
