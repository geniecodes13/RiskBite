#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Print env vars
print("Environment Variables:")
print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')}")
print(f"GOOGLE_CLIENT_SECRET: {os.getenv('GOOGLE_CLIENT_SECRET')}")
print(f"FRONTEND_URL: {os.getenv('FRONTEND_URL')}")

# Check if they're set
if os.getenv('GOOGLE_CLIENT_ID') and os.getenv('GOOGLE_CLIENT_SECRET'):
    print("\n✅ OAuth credentials are loaded!")
else:
    print("\n❌ OAuth credentials NOT loaded!")
