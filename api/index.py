import sys
import os

# Add parent directory to sys.path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main Flask app
from app import app

# Initialize database tables for Vercel serverless environment
try:
    from models import db
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️ Database initialization error: {e}")

# This is the WSGI entry point for Vercel
# Vercel will call this as a serverless function
