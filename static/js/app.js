document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceWaveBtn = document.getElementById('voice-wave-btn');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const voiceControls = document.querySelector('.voice-controls');

    function createSendButton() {
        const sendBtn = document.createElement('button');
        sendBtn.id = 'send-btn';
        sendBtn.className = 'voice-btn send-active';
        sendBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7 11l5-5 5 5"/>
                <path d="M12 18V6"/>
            </svg>
        `;
        sendBtn.title = 'Send message';
        sendBtn.style.background = '#000000';
        sendBtn.style.color = 'white';
        sendBtn.style.borderColor = '#000000';
        sendBtn.addEventListener('click', sendMessage);
        return sendBtn;
    }

    function showSendButton() {
        const existingSendBtn = document.getElementById('send-btn');
        if (!existingSendBtn) {
            voiceControls.innerHTML = '';
            const sendBtn = createSendButton();
            voiceControls.appendChild(sendBtn);
        }
    }

    function showVoiceButtons() {
        const existingSendBtn = document.getElementById('send-btn');
        if (existingSendBtn) {
            voiceControls.innerHTML = `
                <button class="voice-btn" id="voice-btn" title="Voice input">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z"/>
                        <path d="M19 10v1a7 7 0 0 1-14 0v-1"/>
                        <path d="M12 18v4"/>
                        <path d="M8 22h8"/>
                    </svg>
                </button>
                <button class="voice-btn" id="voice-wave-btn" title="Voice wave">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M3 12h18"/>
                        <path d="M3 6h18"/>
                        <path d="M3 18h18"/>
                    </svg>
                </button>
            `;
            // Re-attach event listeners
            document.getElementById('voice-btn').addEventListener('click', handleVoiceInput);
            document.getElementById('voice-wave-btn').addEventListener('click', getNews);
        }
    }

    function addMessage(message, isUser = false) {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
            chatMessages.style.justifyContent = 'flex-start';
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const avatar = document.createElement('div');
        avatar.className = `message-avatar ${isUser ? 'user-avatar' : 'ai-avatar'}`;
        avatar.textContent = isUser ? 'U' : 'T';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Handle formatting for better readability
        if (message.includes('\n')) {
            // Replace line breaks with proper HTML breaks and handle markdown-style formatting
            const formattedMessage = message
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/`(.*?)`/g, '<code>$1</code>');
            
            content.innerHTML = '<p>' + formattedMessage + '</p>';
        } else {
            content.textContent = message;
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        typingIndicator.classList.add('show');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTyping() {
        typingIndicator.classList.remove('show');
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';
        showVoiceButtons(); // Switch back to voice buttons
        showTyping();

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTyping();
            if (data.response) {
                addMessage(data.response);
            } else if (data.error) {
                addMessage('Error: ' + data.error);
            }
        })
        .catch(error => {
            hideTyping();
            addMessage('Error: ' + error.message);
        });
    }

    function handleVoiceInput() {
        addMessage('Voice input activated', true);
        addMessage("I'm listening... (Voice feature coming soon!)");
    }

    function getNews() {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
            chatMessages.style.justifyContent = 'flex-start';
        }
        
        addMessage('Get latest news', true);
        showTyping();
        
        fetch('/news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: 'technology trends' })
        })
        .then(response => response.json())
        .then(data => {
            hideTyping();
            if (data.news) {
                addMessage(data.news);
            } else if (data.error) {
                addMessage('Error: ' + data.error);
            }
        })
        .catch(error => {
            hideTyping();
            addMessage('Error: ' + error.message);
        });
    }

    // Event listeners
    userInput.addEventListener('input', function() {
        if (this.value.trim()) {
            showSendButton();
        } else {
            showVoiceButtons();
        }
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial event listeners for voice buttons
    voiceBtn.addEventListener('click', handleVoiceInput);
    voiceWaveBtn.addEventListener('click', getNews);

    userInput.focus();
});
