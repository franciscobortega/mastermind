"use strict";

const socket = io();

const messages = document.getElementById("messages");
const gameBoard = document.getElementById("game-board");

/**
 * Function to create and display a new message in the lobby.
 * @param {string} name - The name of the user who sent the message.
 * @param {string} msg - The message content to be displayed.
 */
const createMessage = (name, msg, role) => {
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message");

  const messageContent = document.createElement("span");
  messageContent.textContent = `${name}: ${msg}`;

  // Assign message colors based on roles
  switch (role) {
    case "codemaker":
      messageContent.style.color = "red";
      break;
    case "codebreaker":
      messageContent.style.color = "blue";
      break;
    default:
      messageContent.style.backgroundColor = "#ebebeb";
      break;
  }

  messageContainer.appendChild(messageContent);
  messages.appendChild(messageContainer);
};

/**
 * Event listener for incoming "message" events from the WebSocket.
 */
socket.on("message", (data) => {
  createMessage(data.name, data.message, data.role);
});

/**
 * Sends a message to the server using WebSocket.
 */
const sendMessage = () => {
  const message = document.getElementById("message");

  if (message.value === "") return;
  socket.emit("lobby_message", { data: message.value });
  message.value = "";
};

/**
 * Sends the secret code to the server using WebSocket.
 */
const sendCode = () => {
  const codeInput = document.getElementById("secret-input");

  if (codeInput.value === "") return;
  socket.emit("secret_code", { code: codeInput.value });
  codeInput.value = "";
};

socket.on("set_code", (data) => {
  console.log(`secret code: ${data["secret_code"]}`);

  const secretCodeElement = document.getElementById("display-secret-code");
  secretCodeElement.textContent = `The secret code is: ${data["secret_code"]}`;
  secretCodeElement.style.display = "block";

  const secretForm = document.getElementById("secret-form");
  secretForm.remove();
});

/**
 * Sends a guess to the server using WebSocket.
 */
const sendGuess = () => {
  const guessInput = document.getElementById("guess-input");

  if (guessInput.value === "") return;
  socket.emit("multiplayer_guess", { guess: guessInput.value });
  guessInput.value = "";
};

socket.on("update_guesses", (data) => {
  console.log(`${data["name"]} guessed: ${data["guess"]}`);

  const guessesContainer = document.querySelector(".guesses-container");

  const guessElement = document.createElement("li");
  guessElement.textContent = data["guess"];

  guessesContainer.appendChild(guessElement);
});

/**
 * Sends feedback to the server using WebSocket.
 */
const sendFeedback = () => {
  const feedbackNumbersInput = document.getElementById("feedback-nums-input");
  const feedbackLocationsInput = document.getElementById("feedback-locs-input");

  if (feedbackNumbersInput.value === "" || feedbackLocationsInput.value === "")
    return;
  socket.emit("multiplayer_feedback", {
    feedback_numbers: feedbackNumbersInput.value,
    feedback_locations: feedbackLocationsInput.value,
  });
  feedbackNumbersInput.value = "";
  feedbackLocationsInput.value = "";
};

socket.on("update_feedback", (data) => {
  console.log(
    `${data["name"]} said: ${data["feedback-numbers"]} correct numbers, ${data["feedback-locations"]} correct locations.`
  );

  const feedbackContainer = document.querySelector(".feedback-container");

  const guessElement = document.createElement("li");
  guessElement.textContent = `${data["feedback-numbers"]} correct numbers, ${data["feedback-locations"]} correct locations.`;

  feedbackContainer.appendChild(guessElement);
});

const startGame = () => {
  socket.emit("start_game");
};

socket.on("update_room", () => {
  // Hide lobby options
  document.getElementById("lobby-options").style.display = "none";

  // Display the game board
  gameBoard.style.display = "block";
});
