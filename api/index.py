import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Flask app and db
from app import app, db
from flask import jsonify

# Initialize database
try:
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")
except Exception as e:
    print(f"❌ Database initialization error: {str(e)}")

# Vercel serverless function handler
def handler(request):
    # Convert Vercel request to WSGI environment
    from werkzeug.wrappers import Request
    from werkzeug.wsgi import responder
    from werkzeug.test import create_environ
    
    # Create WSGI environment from Vercel request
    environ = create_environ(
        path=request.get('path', '/'),
        base_url=request.get('url', ''),
        query_string=request.get('query', {}),
        method=request.get('method', 'GET'),
        headers=dict(request.get('headers', {})),
        data=request.get('body', b'')
    )
    
    # Create a WSGI application
    @responder
    def application(environ, start_response):
        return app(environ, start_response)
    
    # Call the application
    return application(environ)

# For local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)