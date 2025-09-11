# 🛠️ Thomas AI Agent - Development Guide

## 🚀 Quick Commands (Helper Script)

We provide a helper script to make updates easier:

```bash
python update.py test     # Run all tests
python update.py dev      # Start development server  
python update.py deps     # Update dependencies
python update.py status   # Check git status
python update.py update   # Full update workflow
python update.py help     # Show all commands
```

## 📋 How to Update This Repository

### 1. Setting Up Your Development Environment

```bash
# 1. Clone the repository
git clone https://github.com/shriram1206/AI-Agent.git
cd AI-Agent

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies  
pip install -r requirements.txt

# 4. Set up environment variables (optional)
cp .env.example .env
# Edit .env and add your Perplexity API key if you have one
```

### 2. Testing Your Changes

**Quick way (using helper script):**
```bash
# Test your changes
python update.py test

# Run full update workflow  
python update.py update
```

**Manual way:**
```bash
# Before making any changes - run the test suite to ensure everything works
python test_app.py
```

**After making changes:**
```bash
# 1. Test your changes
python test_app.py

# 2. Run the app locally to verify
python app.py
# Visit http://localhost:5000 to test manually

# 3. Check for any syntax errors
python -m py_compile app.py
```

### 3. Making Updates

#### Code Changes
1. **Edit the files** you need to modify:
   - `app.py` - Main Flask application
   - `templates/index.html` - Frontend HTML
   - `static/css/` - Styling
   - `static/js/` - JavaScript functionality

2. **Test your changes** using the steps above

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push
   ```

#### Adding New Features
1. **Plan your feature** - What does it do? How does it work?
2. **Update `test_app.py`** if needed to test new functionality
3. **Implement the feature** in the appropriate files
4. **Test thoroughly** before committing
5. **Update documentation** if the feature changes how users interact with the app

### 4. Dependencies Management

#### Adding New Dependencies
```bash
# Install the new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt

# Or manually add to requirements.txt with version
echo "package_name==1.2.3" >> requirements.txt
```

#### Updating Dependencies
```bash
# Update a specific package
pip install --upgrade package_name

# Update requirements.txt
pip freeze > requirements.txt

# Test after updates
python test_app.py
```

### 5. Environment Variables

The app uses these environment variables:
- `PERPLEXITY_API_KEY` - Your Perplexity AI API key (optional)
- `DEBUG` - Set to 'True' for development
- `PORT` - Port to run the app on (default: 5000)

### 6. Common Development Tasks

#### Starting Development Server
```bash
# Using the helper script (recommended)
python update.py dev

# Manual way with debug mode (for development)
export DEBUG=True  # On Windows: set DEBUG=True
python app.py

# The app will auto-reload when you make changes
```

#### Testing Different API States
```bash
# Test without API key (demo mode)
unset PERPLEXITY_API_KEY  # On Windows: set PERPLEXITY_API_KEY=
python app.py

# Test with API key
export PERPLEXITY_API_KEY=your_key_here
python app.py
```

### 7. Deployment

#### Local Deployment
```bash
python app.py
```

#### Production Deployment
1. Set `DEBUG=False` in your environment
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

### 8. Troubleshooting

#### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
export PORT=8000  # Use a different port
python app.py
```

**API key issues:**
- The app works without an API key in demo mode
- Check that your `.env` file is properly formatted
- Verify your API key at [Perplexity AI](https://www.perplexity.ai/settings/api)

### 9. Best Practices

1. **Always test** before committing changes
2. **Use meaningful commit messages**
3. **Keep the virtual environment** updated
4. **Don't commit** `.env` files with real API keys
5. **Update documentation** when you change functionality
6. **Keep changes small** and focused on one feature/fix at a time

### 10. Getting Help

If you run into issues:
1. Check the error messages carefully
2. Run `python test_app.py` to isolate the problem
3. Check that all dependencies are installed correctly
4. Verify your Python version (3.7+ required)

---

**Happy coding! 🚀**