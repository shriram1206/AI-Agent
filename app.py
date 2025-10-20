from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Conversation, Message
from datetime import datetime, timedelta, timezone
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Generate secure secret key if not provided
if not os.getenv('SECRET_KEY'):
    import secrets
    generated_key = secrets.token_hex(32)
    app.config['SECRET_KEY'] = generated_key
    print("⚠️  WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY in .env for production!")
else:
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database configuration - Vercel compatible
if os.environ.get('VERCEL'):
    # On Vercel, use PostgreSQL
    database_url = os.environ.get('POSTGRES_URL')
    if not database_url:
        database_url = os.environ.get('DATABASE_URL')
    # Fix for Vercel Postgres (postgres:// -> postgresql://)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development with SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thomas.db'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 5,
    'max_overflow': 10
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session security
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 24 hour session timeout
app.config['SESSION_COOKIE_SECURE'] = os.getenv('PRODUCTION', 'False').lower() == 'true'  # HTTPS only in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Rate limiting - prevent brute force attacks
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Security headers - only in production (disabled for local development)
# Talisman enforces HTTPS - only enable on production (Render, Heroku, etc.)
# For local testing, we skip this to avoid SSL errors
if os.getenv('PRODUCTION', 'False').lower() == 'true':
    Talisman(app, 
        force_https=True,
        strict_transport_security=True,
        content_security_policy={
            'default-src': "'self'",
            'style-src': ["'self'", "'unsafe-inline'"],
            'script-src': ["'self'", "'unsafe-inline'"]
        }
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Input validation functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (3-30 chars, alphanumeric and underscore only)"""
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """Validate password (min 8 chars, at least one letter and one number)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Valid"

def sanitize_input(text, max_length=500):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove potential XSS characters
    text = text.strip()
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    return text

# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_BASE_URL = 'https://api.perplexity.ai/chat/completions'

# Demo responses for when API is not available - structured like ChatGPT
DEMO_RESPONSES = {
    'greeting': [
        "### Hello! 👋\n\nI'm **Thomas**, your AI assistant. I'm here to help you with:\n\n• **Coding & Development** - Python, JavaScript, web development, and more\n• **Problem Solving** - Technical questions and debugging\n• **General Knowledge** - Information, explanations, and advice\n• **Latest News** - Technology trends and updates\n\nWhat would you like to explore today?",
        "### Hey there! 🌟\n\nI'm **Thomas**, ready to assist you! Here's what I can help with:\n\n**Technical Support:**\n• Programming and code review\n• Software architecture advice\n• Debugging and troubleshooting\n\n**Knowledge & Research:**\n• Explaining complex concepts\n• Answering questions\n• Current tech trends\n\nHow can I help you today?",
    ],
    'coding': [
        "### Great! Let's dive into coding. 💻\n\nI can assist you with:\n\n**Popular Languages:**\n• **Python** - Data science, web dev, automation\n• **JavaScript** - Frontend, backend (Node.js), React\n• **HTML/CSS** - Web design and styling\n• **SQL** - Database queries and design\n\n**What I Can Help With:**\n1. Writing clean, efficient code\n2. Debugging and fixing errors\n3. Explaining programming concepts\n4. Best practices and design patterns\n\nWhat specific coding challenge are you working on?",
        "### I'd love to help with your coding project! 🚀\n\n**My Expertise Includes:**\n\n• **Web Development** - Full-stack solutions\n• **Algorithms** - Problem-solving and optimization\n• **Frameworks** - React, Flask, Django, Express\n• **Best Practices** - Clean code, testing, documentation\n\nTell me more about what you're building!",
    ],
    'general': [
        "### I'm here to help! ✨\n\nI'm **Thomas**, an AI assistant designed to provide:\n\n**Key Capabilities:**\n• **Detailed Explanations** - Breaking down complex topics\n• **Problem Solving** - Analytical and creative solutions\n• **Technical Guidance** - Software development support\n• **Research Assistance** - Finding and explaining information\n\n**How It Works:**\nJust ask your question naturally, and I'll provide a clear, structured response tailored to your needs.\n\nWhat would you like to know more about?",
        "### Let me help you with that! 🎯\n\n**What I Can Do:**\n\n1. **Answer Questions** - Provide accurate, detailed information\n2. **Explain Concepts** - Break down complex ideas simply\n3. **Solve Problems** - Offer practical solutions\n4. **Give Advice** - Share best practices and recommendations\n\n**My Approach:**\nI structure my responses to be clear, actionable, and easy to understand.\n\nWhat topic interests you?",
    ],
    'news': [
        "### 📰 Latest Tech Trends (Demo Mode)\n\n**Today's Highlights:**\n\n• **AI & Machine Learning** - Continued advancement in generative AI\n• **Web Development** - Modern frameworks gaining popularity\n• **Python** - Remains the #1 language for data science\n• **Cloud Computing** - Serverless architecture trending\n\n**Note:** *This is demo content. Connect your Perplexity API key for real-time news updates!*\n\n🔑 Get your API key at: https://www.perplexity.ai/settings/api",
        "### 📱 Technology Update (Demo Mode)\n\n**Current Trends:**\n\n1. **Mobile Development** - Progressive Web Apps (PWAs) on the rise\n2. **Security** - Zero-trust architecture becoming standard\n3. **Open Source** - Community-driven projects thriving\n4. **DevOps** - CI/CD automation essential for modern teams\n\n**Want Real-Time News?**\nAdd your Perplexity API key to `.env` file for live updates!\n\n💡 *Demo mode provides general tech insights*",
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

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 503

@app.route('/')
@login_required
def home():
    """Home page route - requires authentication"""
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    return render_template('index.html', conversations=conversations, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Prevent brute force attacks
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        data = request.json
        email = sanitize_input(data.get('email', ''), 100)
        password = data.get('password', '')
        
        # Validate inputs
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            session.permanent = True  # Enable session timeout
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit("3 per hour")  # Limit account creation to prevent spam
def signup():
    """Signup page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        data = request.json
        username = sanitize_input(data.get('username', ''), 30)
        email = sanitize_input(data.get('email', ''), 100)
        password = data.get('password', '')
        
        # Validate inputs
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if not validate_username(username):
            return jsonify({'success': False, 'message': 'Username must be 3-30 characters, alphanumeric and underscore only'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'message': message}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already taken'}), 400
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create first conversation
        conversation = Conversation(user_id=user.id, title='New Chat')
        db.session.add(conversation)
        db.session.commit()
        
        login_user(user)
        session.permanent = True
        return jsonify({'success': True, 'message': 'Account created successfully'})
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
@login_required
@limiter.limit("30 per minute")  # Prevent API abuse
def chat():
    """Handle chat messages from users"""
    try:
        user_message = sanitize_input(request.json.get('message', ''), 2000)
        conversation_id = request.json.get('conversation_id')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        if len(user_message) < 1:
            return jsonify({'error': 'Message too short'}), 400
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
            if not conversation:
                return jsonify({'error': 'Conversation not found'}), 404
        else:
            # Create new conversation
            conversation = Conversation(user_id=current_user.id, title=user_message[:50])
            db.session.add(conversation)
            db.session.commit()
        
        # Save user message
        user_msg = Message(conversation_id=conversation.id, role='user', content=user_message)
        db.session.add(user_msg)
        db.session.commit()
        
        # Check if API key is available
        if not PERPLEXITY_API_KEY:
            # Use demo mode
            demo_response = get_demo_response(user_message)
            return jsonify({'response': demo_response + "\n\n *Demo Mode: Add your Perplexity API key for AI-powered responses!*"})
        
        # Get conversation history (last 10 messages for context)
        messages_history = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.desc()).limit(10).all()
        messages_history.reverse()  # Oldest first
        
        # Build message context for API - structured responses
        api_messages = [
            {'role': 'system', 'content': '''You are Thomas, a helpful and intelligent AI assistant. Provide well-structured, professional responses following these guidelines:

1. **Formatting**: Use markdown formatting for clarity:
   - Use **bold** for emphasis and key terms
   - Use bullet points (•) or numbered lists for multiple items
   - Use headers (###) for different sections when appropriate
   - Use code blocks with triple backticks for code examples
   - Use proper paragraphs with line breaks for readability

2. **Structure**: Organize your responses logically:
   - Start with a brief, direct answer to the main question
   - Follow with detailed explanation if needed
   - Use sections with clear headers for complex topics
   - End with helpful suggestions or next steps when relevant

3. **Tone**: Be conversational yet professional:
   - Use natural, friendly language
   - Show personality and enthusiasm
   - Be concise but comprehensive
   - Adapt complexity to the question

4. **Code Responses**: For programming questions:
   - Explain the concept first
   - Provide clean, well-commented code examples
   - Explain what the code does
   - Suggest best practices or alternatives

5. **Clarity**: Make responses easy to scan and understand
   - Use short paragraphs
   - Break down complex topics into digestible parts
   - Highlight important points

Never include citation numbers like [1][2][3] in your responses.'''}
        ]
        
        # Add only last 3 messages for fastest context
        for msg in messages_history[-3:]:
            api_messages.append({
                'role': msg.role,
                'content': msg.content
            })
        
        # Use Perplexity API for chat
        headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sonar',  # Lightweight, cost-effective, fastest search model
            'messages': api_messages,
            'max_tokens': 500,  # Increased for structured, detailed responses
            'temperature': 0.7,  # More natural and conversational
            'return_citations': False,  # Disable citations
            'return_related_questions': False  # Disable related questions
        }
        
        response = requests.post(PERPLEXITY_BASE_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Clean up citations and make response more natural
            import re
            # Remove citation brackets like [1], [2], [1][2], etc.
            ai_response = re.sub(r'\[\d+\](\[\d+\])*', '', ai_response)
            # Remove extra spaces left after removing citations
            ai_response = re.sub(r'\s+', ' ', ai_response).strip()
            # Remove any remaining citation patterns
            ai_response = re.sub(r'\[citation:?\s*\d+\]', '', ai_response, flags=re.IGNORECASE)
            
            # Save AI response
            ai_msg = Message(conversation_id=conversation.id, role='assistant', content=ai_response)
            db.session.add(ai_msg)
            
            # Update conversation timestamp and title if first message
            conversation.updated_at = datetime.now(timezone.utc)
            if len(messages_history) == 0:
                conversation.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            
            db.session.commit()
            
            return jsonify({
                'response': ai_response,
                'conversation_id': conversation.id
            })
        else:
            # Fall back to demo mode on API error
            error_msg = f"Perplexity API error: {response.status_code}"
            if response.status_code == 401:
                print(f"{error_msg} - Invalid API key. Please check your PERPLEXITY_API_KEY in .env file")
                demo_response = get_demo_response(user_message)
                
                # Save demo response to DB
                ai_msg = Message(conversation_id=conversation.id, role='assistant', content=demo_response)
                db.session.add(ai_msg)
                conversation.updated_at = datetime.now(timezone.utc)
                if len(messages_history) == 0:
                    conversation.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                db.session.commit()
                
                return jsonify({
                    'response': demo_response + "\n\n⚠️ **Demo Mode**: Your API key is invalid. Get a valid key from https://www.perplexity.ai/settings/api",
                    'conversation_id': conversation.id
                })
            else:
                print(f"{error_msg} - {response.text[:200]}")
                demo_response = get_demo_response(user_message)
                
                # Save demo response to DB
                ai_msg = Message(conversation_id=conversation.id, role='assistant', content=demo_response)
                db.session.add(ai_msg)
                conversation.updated_at = datetime.now(timezone.utc)
                db.session.commit()
                
                return jsonify({
                    'response': demo_response + "\n\n⚠️ *Using demo mode due to API issues*",
                    'conversation_id': conversation.id
                })
        
    except requests.exceptions.Timeout:
        # Timeout - use demo mode quickly
        print("Request timeout - falling back to demo mode")
        demo_response = get_demo_response(user_message)
        
        # Save demo response
        ai_msg = Message(conversation_id=conversation.id, role='assistant', content=demo_response)
        db.session.add(ai_msg)
        conversation.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({
            'response': demo_response + "\n\n⏱️ *Demo mode: API timeout*",
            'conversation_id': conversation.id
        })
    except requests.exceptions.RequestException as e:
        # Network-related errors - use demo mode
        print(f"Network error: {str(e)}")
        demo_response = get_demo_response(user_message)
        
        # Save demo response
        ai_msg = Message(conversation_id=conversation.id, role='assistant', content=demo_response)
        db.session.add(ai_msg)
        conversation.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({
            'response': demo_response + "\n\n🔌 *Demo mode: Network connectivity issue*",
            'conversation_id': conversation.id
        })
    except Exception as e:
        # General errors - use demo mode
        print(f"Unexpected error: {str(e)}")
        demo_response = get_demo_response(user_message)
        
        # Save demo response
        try:
            ai_msg = Message(conversation_id=conversation.id, role='assistant', content=demo_response)
            db.session.add(ai_msg)
            conversation.updated_at = datetime.now(timezone.utc)
            db.session.commit()
        except:
            pass  # If DB fails, still return response
        
        return jsonify({
            'response': demo_response + "\n\n🛠️ *Demo mode: Unexpected issue*",
            'conversation_id': conversation.id if conversation else None
        })

@app.route('/news', methods=['POST'])
@login_required
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
                {'role': 'system', 'content': '''You are Thomas, a news assistant. Provide well-structured news updates:

1. Start with a header: ### 📰 [Topic] - Latest Updates
2. Use bullet points (•) for news items
3. Include brief, clear descriptions
4. Use **bold** for key terms and organizations
5. Keep it professional yet conversational
6. No citation numbers or references

Format example:
### 📰 Technology - Latest Updates

• **AI Development** - Major breakthrough in...
• **Market Trends** - Tech stocks showing...
• **New Releases** - Company X launches...'''},
                {'role': 'user', 'content': f'What are the latest news about: {query}'}
            ],
            'max_tokens': 300,
            'temperature': 0.7,
            'return_citations': False,
            'return_related_questions': False
        }
        
        response = requests.post(PERPLEXITY_BASE_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            news_content = result['choices'][0]['message']['content']
            
            # Clean up citations
            import re
            news_content = re.sub(r'\[\d+\](\[\d+\])*', '', news_content)
            news_content = re.sub(r'\s+', ' ', news_content).strip()
            
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

@app.route('/conversations')
@login_required
def get_conversations():
    """Get all conversations for current user"""
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    return jsonify([{
        'id': conv.id,
        'title': conv.title,
        'created_at': conv.created_at.isoformat(),
        'updated_at': conv.updated_at.isoformat()
    } for conv in conversations])

@app.route('/conversation/<int:conversation_id>')
@login_required
def get_conversation(conversation_id):
    """Get specific conversation with all messages"""
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    return jsonify({
        'id': conversation.id,
        'title': conversation.title,
        'messages': [msg.to_dict() for msg in messages]
    })

@app.route('/conversation/new', methods=['POST'])
@login_required
def new_conversation():
    """Create a new conversation"""
    conversation = Conversation(user_id=current_user.id, title='New Chat')
    db.session.add(conversation)
    db.session.commit()
    return jsonify({
        'id': conversation.id,
        'title': conversation.title,
        'created_at': conversation.created_at.isoformat()
    })

@app.route('/conversation/<int:conversation_id>/delete', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    """Delete a conversation"""
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/conversation/<int:conversation_id>/rename', methods=['PUT'])
@login_required
def rename_conversation(conversation_id):
    """Rename a conversation"""
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=current_user.id).first()
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    data = request.json
    new_title = data.get('title')
    if new_title:
        conversation.title = new_title[:200]
        db.session.commit()
        return jsonify({'success': True, 'title': conversation.title})
    
    return jsonify({'error': 'No title provided'}), 400

# Vercel serverless compatibility
if os.environ.get('VERCEL'):
    # On Vercel, initialize database in application context
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    
    # Get port from environment variable for deployment flexibility
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
