# Thomas - Personal Agent 🤖

A modern AI-powered personal assistant built with Flask and Perplexity AI. Thomas can help with coding questions, lifestyle advice, and provide real-time news updates.

![Thomas Personal Agent](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)

## ✨ Features

- 💬 **Smart Chat** - Conversational AI powered by Perplexity
- 📰 **Live News** - Real-time news and trends
- 📱 **Mobile Friendly** - Works on all devices  
- 🎨 **Modern UI** - Beautiful interface with smooth animations

## 🚀 Quick Start

1. **Clone and install**
   ```bash
   git clone https://github.com/shriram1206/AI-Agent.git
   cd AI-Agent
   pip install -r requirements.txt
   ```

2. **Test your setup** *(recommended)*
   ```bash
   python test_app.py
   ```

3. **Add your API key** *(optional - works without it!)*
   ```bash
   cp .env.example .env
   # Edit .env and add your Perplexity API key
   ```

4. **Run Thomas**
   ```bash
   python app.py
   ```
   
5. **Chat with Thomas** at `http://localhost:5000`

## � API Key Setup

- **Without API key**: Thomas works in demo mode with smart responses
- **With API key**: Get real AI-powered responses from Perplexity
- **Get your key**: Sign up at [Perplexity AI](https://www.perplexity.ai/settings/api)

## 📁 Project Structure

```
AI-Agent/
├── app.py              # Main Flask app
├── requirements.txt    # Dependencies  
├── .env.example       # API key template
├── test_app.py        # Test suite
├── DEVELOPMENT.md     # Update & development guide
├── static/            # CSS & JavaScript
└── templates/         # HTML files
```

## 🔄 How to Update This Repository

**Need to make changes?** 📖 Read the [UPDATE_GUIDE.md](UPDATE_GUIDE.md) for step-by-step instructions!

**Quick update workflow:**
1. `python update.py test` - Test before changes
2. Make your changes
3. `python update.py test` - Test after changes  
4. `git add . && git commit -m "Your changes"`
5. `git push`

**For developers:** Check out [DEVELOPMENT.md](DEVELOPMENT.md) for the complete development guide.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📝 License

MIT License - feel free to use and modify!

---

**Built with ❤️ using Python and Perplexity AI**
