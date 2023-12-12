"use strict";

const socket = io();

const messages = document.getElementById("messages");
const gameBoard = document.getElementById("game-board");

/**
 * Function to create and display a new message in the lobby.
 * @param {string} name - The name of the user who sent the message.
 * @param {string} msg - The message content to be displayed.
 */
const createMessage = (name, msg) => {
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message");

  const messageContent = document.createElement("span");
  messageContent.textContent = `${name}: ${msg}`;

  messageContainer.appendChild(messageContent);
  messages.appendChild(messageContainer);
};

/**
 * Event listener for incoming "message" events from the WebSocket.
 */
socket.on("message", (data) => {
  createMessage(data.name, data.message);
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

/**
 * Sends feedback to the server using WebSocket.
 */
const sendFeedback = () => {
  const feedbackInput = document.getElementById("feedback-input");

  if (feedbackInput.value === "") return;
  socket.emit("multiplayer_feedback", { feedback: feedbackInput.value });
  feedbackInput.value = "";
};

const startGame = () => {
  socket.emit("start_game");
};

socket.on("update_room", () => {
  // Hide lobby options
  document.getElementById("lobby-options").style.display = "none";

  // Display the game board
  gameBoard.style.display = "block";
});
