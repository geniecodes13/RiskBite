"""
FastAPI startup script for Windows
Run this to start the backend server
"""

import os
import subprocess
import sys
import webbrowser
import time

def main():
    """Start the RISKbite backend server"""
    
    print("=" * 60)
    print("🥗 RISKbite Backend - Starting Server")
    print("=" * 60)
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  WARNING: Virtual environment not activated!")
        print("Please activate with: venv\\Scripts\\activate")
        print()
    
    # Check dependencies
    print("\n✓ Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import pytesseract
        import pydantic
        print("✓ All dependencies installed!")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check Tesseract
    print("\n✓ Checking Tesseract OCR...")
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        print("✓ Tesseract OCR found!")
        print(f"  Version: {result.stdout.split()[0]}")
    except FileNotFoundError:
        print("⚠️  Tesseract OCR not found in PATH!")
        print("Please install from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("And set TESSERACT_CMD environment variable in .env")
    
    # Start server
    print("\n" + "=" * 60)
    print("🚀 Starting FastAPI server...")
    print("=" * 60)
    print("\n📍 Server running at: http://localhost:8000")
    print("📖 API Docs at: http://localhost:8000/docs")
    print("🔄 Server will reload on code changes")
    print("\nPress CTRL+C to stop server\n")
    
    # Open browser after delay
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:8000/docs')
    except:
        pass
    
    # Start server
    try:
        os.chdir(os.path.dirname(__file__))
        os.system('python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000')
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
