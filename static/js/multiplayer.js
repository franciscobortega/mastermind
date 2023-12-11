"use strict";

const socket = io();

const messages = document.getElementById("messages");

/**
 * Function to create and display a new message in the lobby.
 * @param {string} name - The name of the user who sent the message.
 * @param {string} msg - The message content to be displayed.
 */
const createMessage = (name, msg) => {
  const content = `
  <div class="message">
    <span>${name}: ${msg}</span>
  </div>
  `;

  messages.innerHTML += content;
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
