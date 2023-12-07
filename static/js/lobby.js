"use strict";

console.log("lobby js...");

const socket = io();

socket.on("connect", () => {
  console.log("Connected to WebSocket");
});

socket.on("disconnect", () => {
  console.log("Disconnected from WebSocket");
});
