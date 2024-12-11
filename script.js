const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("userInput");

async function sendMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage) {
    // Display user message
    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user");
    userMessageElement.textContent = userMessage;
    chatBox.appendChild(userMessageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
    userInput.value = "";

    try {
      // Send message to backend and get response
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();

      // Display bot response
      const botMessageElement = document.createElement("div");
      botMessageElement.classList.add("message", "bot");
      botMessageElement.textContent = data.response;
      chatBox.appendChild(botMessageElement);

      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
      console.error("Error communicating with the backend:", error);

      const errorMessageElement = document.createElement("div");
      errorMessageElement.classList.add("message", "bot");
      errorMessageElement.textContent = "Oops! Something went wrong.";
      chatBox.appendChild(errorMessageElement);
    }
  }
}

// Send message on Enter key press
userInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});
