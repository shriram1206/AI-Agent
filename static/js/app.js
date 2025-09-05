document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const newsBtn = document.getElementById('news-btn');
    const chatMessages = document.getElementById('chat-messages');

    function addMessage(message, isUser = false) {
        const welcomeMsg = document.querySelector('.welcome-message');
        if (welcomeMsg && !isUser) {
            welcomeMsg.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response);
            } else if (data.error) {
                addMessage('Error: ' + data.error);
            }
        })
        .catch(error => {
            addMessage('Error: ' + error.message);
        });
    }

    function getNews() {
        addMessage('Getting latest news...', true);
        
        fetch('/news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: 'technology trends' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.news) {
                addMessage(data.news);
            } else if (data.error) {
                addMessage('Error: ' + data.error);
            }
        })
        .catch(error => {
            addMessage('Error: ' + error.message);
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    newsBtn.addEventListener('click', getNews);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    userInput.focus();
});
