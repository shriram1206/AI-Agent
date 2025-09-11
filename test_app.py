#!/usr/bin/env python3
"""
Simple test script for Thomas AI Agent
Run this to verify your installation and changes are working correctly.
"""

import sys
import json
import requests
from app import app

def test_flask_app():
    """Test the Flask application endpoints"""
    print("🧪 Testing Thomas AI Agent...")
    
    # Test app creation
    try:
        with app.test_client() as client:
            print("✅ Flask app created successfully")
            
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads correctly")
            else:
                print(f"❌ Home page failed: {response.status_code}")
                return False
            
            # Test chat endpoint with demo mode
            chat_data = {"message": "Hello Thomas"}
            response = client.post('/chat', 
                                 data=json.dumps(chat_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                if 'response' in result:
                    print("✅ Chat endpoint works correctly")
                    print(f"   📝 Response: {result['response'][:100]}...")
                else:
                    print("❌ Chat response missing 'response' field")
                    return False
            else:
                print(f"❌ Chat endpoint failed: {response.status_code}")
                return False
            
            # Test news endpoint
            news_data = {"query": "technology"}
            response = client.post('/news',
                                 data=json.dumps(news_data), 
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                if 'news' in result:
                    print("✅ News endpoint works correctly")
                    print(f"   📰 News: {result['news'][:100]}...")
                else:
                    print("❌ News response missing 'news' field")
                    return False
            else:
                print(f"❌ News endpoint failed: {response.status_code}")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_modules = ['flask', 'requests', 'dotenv']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} is installed")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} is missing")
    
    if missing_modules:
        print(f"\n📦 Please install missing modules: pip install {' '.join(missing_modules)}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Thomas AI Agent - Test Suite")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    print("\n🧪 Running application tests...")
    print("-" * 30)
    
    # Test the Flask app
    if test_flask_app():
        print("\n🎉 All tests passed! Your Thomas AI Agent is working correctly.")
        print("💡 You can now run: python app.py")
        return True
    else:
        print("\n❌ Some tests failed. Please check your setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)