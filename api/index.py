# Vercel serverless function entry point
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Initialize database for Vercel
with app.app_context():
    from models import db
    db.create_all()

# Vercel expects the Flask app to be available as 'app'
# This is the entry point for serverless deployment
