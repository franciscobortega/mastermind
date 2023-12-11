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
