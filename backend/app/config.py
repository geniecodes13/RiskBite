"""
Optional: Configuration for environment-based settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_ENV = os.getenv("API_ENV", "development")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Image Processing
MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", 10))
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

# Tesseract Configuration (optional)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", None)
if TESSERACT_PATH:
    import pytesseract
    pytesseract.pytesseract.pytesseract_cmd = TESSERACT_PATH
