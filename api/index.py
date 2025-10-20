import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app
from app import app

# Initialize database
try:
    from models import db
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"DB init error: {e}")
