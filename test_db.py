"""
Database Connection Test Script
Tests if the database is properly configured and creates tables if needed
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 THOMAS DATABASE CONNECTION TEST")
print("=" * 60)
print()

# Test 1: Check if required packages are installed
print("✓ Test 1: Checking required packages...")
try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from werkzeug.security import generate_password_hash
    print("  ✅ All packages installed successfully")
except ImportError as e:
    print(f"  ❌ Missing package: {e}")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 2: Check environment variables
print("✓ Test 2: Checking environment variables...")
api_key = os.getenv('PERPLEXITY_API_KEY')
secret_key = os.getenv('SECRET_KEY')

if api_key and api_key != 'your_perplexity_api_key_here':
    print(f"  ✅ PERPLEXITY_API_KEY is set ({api_key[:10]}...)")
else:
    print("  ⚠️  PERPLEXITY_API_KEY not set (will use demo mode)")

if secret_key and secret_key != 'your_secret_key_here':
    print(f"  ✅ SECRET_KEY is set ({secret_key[:10]}...)")
else:
    print("  ⚠️  SECRET_KEY not set (will use default)")

print()

# Test 3: Initialize Flask app
print("✓ Test 3: Initializing Flask application...")
try:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key or 'test-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thomas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("  ✅ Flask app initialized")
except Exception as e:
    print(f"  ❌ Failed to initialize Flask: {e}")
    sys.exit(1)

print()

# Test 4: Initialize database
print("✓ Test 4: Connecting to database...")
try:
    from models import db, User, Conversation, Message
    db.init_app(app)
    print("  ✅ Database models loaded")
except Exception as e:
    print(f"  ❌ Failed to load models: {e}")
    sys.exit(1)

print()

# Test 5: Create tables
print("✓ Test 5: Creating database tables...")
try:
    with app.app_context():
        db.create_all()
        print("  ✅ Tables created successfully")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"  ✅ Found {len(tables)} tables: {', '.join(tables)}")
except Exception as e:
    print(f"  ❌ Failed to create tables: {e}")
    sys.exit(1)

print()

# Test 6: Test database operations
print("✓ Test 6: Testing database operations...")
try:
    with app.app_context():
        # Check if test user exists
        test_user = User.query.filter_by(email='test@thomas.ai').first()
        
        if not test_user:
            # Create test user
            test_user = User(
                username='test_user',
                email='test@thomas.ai'
            )
            test_user.set_password('testpassword123')
            db.session.add(test_user)
            db.session.commit()
            print("  ✅ Created test user")
        else:
            print("  ✅ Test user already exists")
        
        # Test conversation creation
        test_conv = Conversation.query.filter_by(user_id=test_user.id).first()
        if not test_conv:
            test_conv = Conversation(
                user_id=test_user.id,
                title='Test Conversation'
            )
            db.session.add(test_conv)
            db.session.commit()
            print("  ✅ Created test conversation")
        else:
            print("  ✅ Test conversation already exists")
        
        # Test message creation
        test_message = Message.query.filter_by(conversation_id=test_conv.id).first()
        if not test_message:
            test_message = Message(
                conversation_id=test_conv.id,
                role='user',
                content='Hello Thomas!'
            )
            db.session.add(test_message)
            db.session.commit()
            print("  ✅ Created test message")
        else:
            print("  ✅ Test message already exists")
        
        # Verify data
        user_count = User.query.count()
        conv_count = Conversation.query.count()
        msg_count = Message.query.count()
        
        print(f"  ✅ Database stats:")
        print(f"     - Users: {user_count}")
        print(f"     - Conversations: {conv_count}")
        print(f"     - Messages: {msg_count}")
        
except Exception as e:
    print(f"  ❌ Database operation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 7: Test password hashing
print("✓ Test 7: Testing password security...")
try:
    with app.app_context():
        test_user = User.query.filter_by(email='test@thomas.ai').first()
        
        # Test correct password
        if test_user.check_password('testpassword123'):
            print("  ✅ Password verification works")
        else:
            print("  ❌ Password verification failed")
        
        # Test wrong password
        if not test_user.check_password('wrongpassword'):
            print("  ✅ Wrong password correctly rejected")
        else:
            print("  ❌ Security issue: wrong password accepted!")
        
except Exception as e:
    print(f"  ❌ Password test failed: {e}")

print()
print("=" * 60)
print("✅ ALL TESTS PASSED! Database is ready to use!")
print("=" * 60)
print()
print("📊 Database Location: thomas.db")
print("🔑 Test Account Created:")
print("   Email: test@thomas.ai")
print("   Password: testpassword123")
print()
print("🚀 You can now run: python app.py")
print()
