#!/usr/bin/env python3
"""
Thomas AI Agent - Update Helper Script
Automates common update tasks for the repository.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def update_dependencies():
    """Update project dependencies"""
    print("\n📦 Updating Dependencies")
    print("-" * 30)
    
    if run_command("pip install -r requirements.txt", "Installing/updating dependencies"):
        run_command("python test_app.py", "Testing after dependency update")

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running Tests")
    print("-" * 20)
    
    run_command("python test_app.py", "Running test suite")

def start_development():
    """Start the development server"""
    print("\n🚀 Starting Development Server")
    print("-" * 35)
    
    # Set debug mode for development
    os.environ['DEBUG'] = 'True'
    
    print("🔧 Debug mode enabled")
    print("🌐 Server will start at http://localhost:5000")
    print("⚡ Auto-reload enabled - changes will be detected automatically")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run("python app.py", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")

def git_status():
    """Check git status and recent changes"""
    print("\n📊 Git Status")
    print("-" * 15)
    
    run_command("git status --porcelain", "Checking for uncommitted changes")
    run_command("git log --oneline -5", "Showing recent commits")

def full_update():
    """Run a complete update workflow"""
    print("🔄 Full Update Workflow")
    print("=" * 25)
    
    steps = [
        ("git status --porcelain", "Checking git status"),
        ("python test_app.py", "Running pre-update tests"),
        ("pip install -r requirements.txt", "Updating dependencies"),
        ("python test_app.py", "Running post-update tests"),
    ]
    
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n❌ Update workflow stopped at: {desc}")
            return False
    
    print("\n🎉 Full update completed successfully!")
    return True

def show_help():
    """Show available commands"""
    print("🛠️  Thomas AI Agent - Update Helper")
    print("=" * 40)
    print("Available commands:")
    print("  deps     - Update dependencies")  
    print("  test     - Run tests")
    print("  dev      - Start development server")
    print("  status   - Check git status")
    print("  update   - Full update workflow")
    print("  help     - Show this help")
    print()
    print("Usage: python update.py [command]")
    print("Example: python update.py test")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'deps': update_dependencies,
        'test': run_tests, 
        'dev': start_development,
        'status': git_status,
        'update': full_update,
        'help': show_help
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()