// Helper function to escape HTML and prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceWaveBtn = document.getElementById('voice-wave-btn');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const voiceControls = document.querySelector('.voice-controls');
    const newChatBtn = document.getElementById('new-chat-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    
    let currentConversationId = null;

    // Load current conversation from URL or create new
    const urlParams = new URLSearchParams(window.location.search);
    const convId = urlParams.get('conversation');
    if (convId) {
        loadConversation(parseInt(convId));
    }

    // Sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.toggle('show');
            
            // Toggle overlay
            let overlay = document.querySelector('.sidebar-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.className = 'sidebar-overlay';
                document.body.appendChild(overlay);
                
                // Close sidebar when clicking overlay
                overlay.addEventListener('click', function() {
                    sidebar.classList.remove('show');
                    overlay.classList.remove('show');
                });
            }
            overlay.classList.toggle('show');
        });
    }

    // New chat button
    if (newChatBtn) {
        newChatBtn.addEventListener('click', createNewConversation);
    }

    // Conversation item clicks
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', function() {
            const convId = this.getAttribute('data-id');
            loadConversation(parseInt(convId));
            
            // Update active state
            document.querySelectorAll('.conversation-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Hide sidebar after selecting conversation
            sidebar.classList.remove('show');
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) {
                overlay.classList.remove('show');
            }
        });
    });

    function createNewConversation() {
        fetch('/conversation/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            currentConversationId = data.id;
            window.history.pushState({}, '', `/?conversation=${data.id}`);
            
            // Clear messages
            chatMessages.innerHTML = `
                <div class="empty-state">
                    <div class="welcome-message">Hey I'm Thomas How can I help you today?</div>
                </div>
            `;
            chatMessages.style.justifyContent = 'center';
            
            // Reload conversations list
            location.reload();
        })
        .catch(error => {
            console.error('Error creating conversation:', error);
        });
    }

    function loadConversation(conversationId) {
        currentConversationId = conversationId;
        window.history.pushState({}, '', `/?conversation=${conversationId}`);
        
        fetch(`/conversation/${conversationId}`)
        .then(response => response.json())
        .then(data => {
            chatMessages.innerHTML = '';
            chatMessages.style.justifyContent = 'flex-start';
            
            if (data.messages.length === 0) {
                chatMessages.innerHTML = `
                    <div class="empty-state">
                        <div class="welcome-message">Hey I'm Thomas How can I help you today?</div>
                    </div>
                `;
                chatMessages.style.justifyContent = 'center';
            } else {
                data.messages.forEach(msg => {
                    addMessage(msg.content, msg.role === 'user');
                });
            }
        })
        .catch(error => {
            console.error('Error loading conversation:', error);
        });
    }

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
        
        if (isUser) {
            // Modern user icon
            avatar.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>`;
        } else {
            avatar.textContent = 'T';
        }
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Enhanced markdown-style formatting for better readability
        let formattedMessage = message;
        
        // Handle code blocks (```code```)
        formattedMessage = formattedMessage.replace(/```(\w+)?\n([\s\S]*?)```/g, function(match, lang, code) {
            return `<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`;
        });
        
        // Handle inline code (`code`)
        formattedMessage = formattedMessage.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Handle headers (### Header)
        formattedMessage = formattedMessage.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
        formattedMessage = formattedMessage.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
        formattedMessage = formattedMessage.replace(/^# (.*?)$/gm, '<h1>$1</h1>');
        
        // Handle bold text (**text**)
        formattedMessage = formattedMessage.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Handle italic text (*text*)
        formattedMessage = formattedMessage.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Handle numbered lists (1. item)
        formattedMessage = formattedMessage.replace(/^\d+\.\s+(.*)$/gm, '<li class="numbered">$1</li>');
        
        // Handle bullet points (• item or - item)
        formattedMessage = formattedMessage.replace(/^[•\-]\s+(.*)$/gm, '<li>$1</li>');
        
        // Wrap consecutive list items in ul/ol
        formattedMessage = formattedMessage.replace(/(<li class="numbered">.*?<\/li>\n?)+/gs, '<ol>$&</ol>');
        formattedMessage = formattedMessage.replace(/(<li>.*?<\/li>\n?)+/gs, '<ul>$&</ul>');
        
        // Handle line breaks and paragraphs
        formattedMessage = formattedMessage.replace(/\n\n/g, '</p><p>');
        formattedMessage = formattedMessage.replace(/\n/g, '<br>');
        
        // Wrap in paragraph if not already formatted
        if (!formattedMessage.includes('<pre>') && !formattedMessage.includes('<h1>') && !formattedMessage.includes('<ul>') && !formattedMessage.includes('<ol>')) {
            formattedMessage = '<p>' + formattedMessage + '</p>';
        }
        
        content.innerHTML = formattedMessage;
        
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
        showVoiceButtons();
        showTyping();

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                conversation_id: currentConversationId
            })
        })
        .then(response => response.json())
        .then(data => {
            hideTyping();
            if (data.response) {
                addMessage(data.response);
                if (data.conversation_id) {
                    currentConversationId = data.conversation_id;
                    window.history.pushState({}, '', `/?conversation=${data.conversation_id}`);
                }
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
    if (voiceBtn) voiceBtn.addEventListener('click', handleVoiceInput);
    if (voiceWaveBtn) voiceWaveBtn.addEventListener('click', getNews);

    userInput.focus();
});

// Global function for deleting conversations
function deleteConversation(conversationId) {
    if (!confirm('Delete this conversation?')) {
        return;
    }

    fetch(`/conversation/${conversationId}/delete`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error deleting conversation:', error);
        alert('Failed to delete conversation');
    });
}
