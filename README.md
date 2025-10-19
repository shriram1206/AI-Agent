# Thomas - Personal AI Agent 🤖

A modern AI-powered personal assistant built with Flask and Perplexity AI. Thomas features user authentication, conversation history management, and ChatGPT-like interface. Perfect for coding help, lifestyle advice, news updates, and general assistance.

![Thomas Personal Agent](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 User Authentication
- Secure login and signup system with password hashing
- Individual user accounts with personal conversation history
- Session management and protected routes

### 💬 ChatGPT-Like Experience
- **Conversation Threads** - Create and manage multiple conversations
- **Conversation History** - All messages saved and retrievable
- **Context Memory** - AI remembers last 10 messages in each conversation
- **Smart Responses** - Natural AI that only introduces itself when appropriate
- **Sidebar Navigation** - Easy access to all your conversations

### 📰 Additional Features
- **Real-time News** - Get latest technology trends and updates
- **Voice Controls** - Ready for voice input integration
- **Mobile Responsive** - Seamless experience on all devices
- **Modern UI** - Clean, professional ChatGPT-inspired interface
- **Dark Sidebar** - Beautiful conversation management sidebar

## 🚀 Quick Start

1. **Clone and install**
   ```bash
   git clone https://github.com/shriram1206/AI-Agent.git
   cd AI-Agent
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Perplexity API key and secret key
   ```

3. **Run Thomas**
   ```bash
   python app.py
   ```
   The database will be created automatically on first run.
   
4. **Create an account** at `http://localhost:5000/signup`

5. **Start chatting!** Login and enjoy conversations with Thomas

## 🔑 Environment Setup

Create a `.env` file with:
```env
PERPLEXITY_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_for_sessions
DATABASE_URL=sqlite:///thomas.db  # Or PostgreSQL for production
DEBUG=False
```

- **Get Perplexity API key**: [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
- **Generate SECRET_KEY**: Use Python's `secrets.token_hex(32)`

## 🚢 Deployment (Render.com)

1. Push to GitHub (branch: `main`)
2. Create new Web Service on Render
3. Connect repository: `shriram1206/AI-Agent`
4. Set environment variables in Render dashboard
5. Deploy automatically on push

## 📁 Project Structure

```
AI-Agent/
├── app.py                      # Main Flask application with routes
├── models.py                   # Database models (User, Conversation, Message)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── static/
│   ├── css/
│   │   ├── style.css          # Main chat interface styles
│   │   └── sidebar.css        # Conversation sidebar styles
│   └── js/
│       └── app.js             # Frontend JavaScript logic
├── templates/
│   ├── index.html             # Main chat interface
│   ├── login.html             # Login page
│   └── signup.html            # Signup page
└── thomas.db                  # SQLite database (auto-created)
```

## 🗄️ Database Schema

- **Users**: Authentication and user profiles
- **Conversations**: Chat threads with titles and timestamps
- **Messages**: Individual messages linked to conversations
- **Relationships**: Full conversation history per user

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📝 License

MIT License - feel free to use and modify!

---

**Built with ❤️ using Python and Perplexity AI**
