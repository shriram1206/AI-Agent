from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_BASE_URL = 'https://api.perplexity.ai/chat/completions'

# Demo responses for when API is not available
DEMO_RESPONSES = {
    'greeting': [
        "Hey! I'm Thomas, your personal assistant. How can I help you today?",
        "Hi there! Thomas here. What can I do for you?",
        "Hello! I'm Thomas. Ask me anything!",
        "Hey! Thomas at your service. What's on your mind?"
    ],
    'coding': [
        "I can help with coding! Try asking about Python, JavaScript, HTML, CSS, or any programming language.",
        "Coding questions? I'm here to help! What language are you working with?",
        "I love helping with code! What are you building?"
    ],
    'general': [
        "I'm Thomas, your AI assistant! I can help with coding, lifestyle advice, and general questions.",
        "That's an interesting question! I'd love to help you with that.",
        "I'm here to assist! What would you like to know?",
        "Great question! I'm Thomas, and I'm here to help."
    ],
    'news': [
        "📰 Latest Tech Trends (Demo Mode):\n• AI assistants are becoming more popular\n• Web development continues to evolve\n• Python remains a top programming language\n\n*Connect your API for real-time news!* - Thomas",
        "📱 Tech Update (Demo):\n• Mobile-first design is essential\n• Cloud computing growing rapidly\n• Open source projects thriving\n\n*Real news available with API key!* - Thomas"
    ]
}

def get_demo_response(user_message):
    """Generate demo responses when API is not available"""
    import random
    
    message_lower = user_message.lower()
    
    # Check for greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'howdy', 'greetings']):
        return random.choice(DEMO_RESPONSES['greeting'])
    
    # Check for coding-related queries
    elif any(word in message_lower for word in ['code', 'coding', 'python', 'javascript', 'html', 'css', 'programming', 'bug', 'function']):
        return random.choice(DEMO_RESPONSES['coding'])
    
    # Default general response
    else:
        return random.choice(DEMO_RESPONSES['general'])

def get_demo_news():
    """Generate demo news when API is not available"""
    import random
    return random.choice(DEMO_RESPONSES['news'])

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from users"""
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if API key is available
        if not PERPLEXITY_API_KEY:
            # Use demo mode
            demo_response = get_demo_response(user_message)
            return jsonify({'response': demo_response + "\n\n *Demo Mode: Add your Perplexity API key for AI-powered responses!*"})
        
        # Use Perplexity API for chat
        headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sonar',
            'messages': [
                {'role': 'system', 'content': 'You are Thomas, a helpful AI assistant. Respond naturally and conversationally. Only introduce yourself as Thomas when explicitly greeted or asked who you are. For regular questions, just provide helpful, direct answers without repeatedly saying your name. Keep responses concise, friendly, and informative. Use formatting like bullet points or line breaks when helpful. No citations unless specifically requested.'},
                {'role': 'user', 'content': user_message}
            ],
            'max_tokens': 500
        }
        
        response = requests.post(PERPLEXITY_BASE_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            # Fall back to demo mode on API error
            print(f"Perplexity API error: {response.status_code} - {response.text}")
            demo_response = get_demo_response(user_message)
            return jsonify({'response': demo_response + "\n\n⚠️ *Using demo mode due to API issues*"})
        
    except requests.exceptions.RequestException as e:
        # Network-related errors - use demo mode
        print(f"Network error: {str(e)}")
        demo_response = get_demo_response(user_message)
        return jsonify({'response': demo_response + "\n\n🔌 *Demo mode: Network connectivity issue*"})
    except Exception as e:
        # General errors - use demo mode
        print(f"Unexpected error: {str(e)}")
        demo_response = get_demo_response(user_message)
        return jsonify({'response': demo_response + "\n\n🛠️ *Demo mode: Unexpected issue*"})

@app.route('/news', methods=['POST'])
def get_news():
    """Handle news requests"""
    try:
        query = request.json.get('query', 'latest technology trends')
        
        # Check if API key is available
        if not PERPLEXITY_API_KEY:
            # Use demo mode
            demo_news = get_demo_news()
            return jsonify({'news': demo_news})
        
        # Use Perplexity API for real-time news
        headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sonar',
            'messages': [
                {'role': 'system', 'content': 'You are Thomas, a helpful news assistant. Provide brief, informative news updates with recent information. Use bullet points for clarity. Keep it concise and professional. No need to repeatedly introduce yourself. Focus on the news content with dates when available.'},
                {'role': 'user', 'content': f'Latest news update about: {query}'}
            ],
            'max_tokens': 500
        }
        
        response = requests.post(PERPLEXITY_BASE_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            news_content = result['choices'][0]['message']['content']
            return jsonify({'news': news_content})
        else:
            # Fall back to demo mode
            print(f"News API error: {response.status_code} - {response.text}")
            demo_news = get_demo_news()
            return jsonify({'news': demo_news})
            
    except requests.exceptions.RequestException as e:
        print(f"Network error in news: {str(e)}")
        demo_news = get_demo_news()
        return jsonify({'news': demo_news})
    except Exception as e:
        print(f"Unexpected error in news: {str(e)}")
        demo_news = get_demo_news()
        return jsonify({'news': demo_news})

if __name__ == '__main__':
    # Get port from environment variable for deployment flexibility
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
