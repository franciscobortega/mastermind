"use strict";

const socket = io();

socket.on("connect", () => {
  console.log("Connected to WebSocket");
});

socket.on("disconnect", () => {
  console.log("Disconnected from WebSocket");
});

// Testing unique identifiers
let uniqueUserId;

socket.on("user_connected", function (data) {
  uniqueUserId = data.user_id;
});

document.getElementById("lobby-form").addEventListener("submit", function (e) {
  e.preventDefault();

  // Extract message from input field
  const messageInput = document.getElementById("testmessage-input");
  const message = messageInput.value;

  // Send the message with unique ID to the backend
  socket.emit("lobby_message", { message, user_id: uniqueUserId });

  testMessaging(message, "Me");
  // Clear the input field
  messageInput.value = "";
});

// WebSocket event for received messages
socket.on("lobby_message", function (data) {
  const { message, user_id } = data;

  testMessaging(message.message, user_id);
});

function testMessaging(message, user_id) {
  // Create a new element for the message
  let newMessage = document.createElement("p");
  newMessage.textContent = `${user_id}: ${message}`;

  // Append the new message
  let messageContainer = document.querySelector("#lobby-form");
  messageContainer.appendChild(newMessage);
}
