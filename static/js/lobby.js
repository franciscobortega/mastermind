"use strict";

const socket = io();

socket.on("connect", () => {
  console.log("Connected to WebSocket");
});

socket.on("disconnect", () => {
  console.log("Disconnected from WebSocket");
});

document.getElementById("lobby-form").addEventListener("submit", function (e) {
  e.preventDefault();

  // Extract message from input field
  const messageInput = document.getElementById("testmessage-input");
  const message = messageInput.value;

  // Send message to server
  socket.emit("lobby_message", message);

  // Clear the input field
  messageInput.value = "";
});

// WebSocket event handling for received messages
socket.on("lobby_message", function (message) {
  testMessaging(message);
});

function testMessaging(message) {
  // Create a new element for the message
  let newMessage = document.createElement("p");
  newMessage.textContent = message;

  // Append the new message
  let messageContainer = document.querySelector("#lobby-form");
  messageContainer.appendChild(newMessage);
}
