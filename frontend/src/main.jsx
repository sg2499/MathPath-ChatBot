import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./styles/chatbot.css";

const rootElementId = "mathpath-chatbot-root";
let rootElement = document.getElementById(rootElementId);

if (!rootElement) {
  rootElement = document.createElement("div");
  rootElement.id = rootElementId;
  document.body.appendChild(rootElement);
}

createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
