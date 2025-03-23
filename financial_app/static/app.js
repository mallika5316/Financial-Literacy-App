// Send message to the chatbot API
function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    // Add the user's message to the chat window
    addMessage('User', userInput);

    // Send the message to the chatbot backend
    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('Chatbot', data.reply);
    })
    .catch(error => {
        addMessage('Chatbot', 'Error occurred. Please try again later.');
        console.error('Error:', error);
    });

    document.getElementById('user-input').value = '';  // Clear the input field
}

// Add messages to the chat window
function addMessage(sender, message) {
    let messageBox = document.getElementById('messages');
    let messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    messageBox.appendChild(messageElement);

    // Scroll to the bottom to show the latest message
    messageBox.scrollTop = messageBox.scrollHeight;
}
