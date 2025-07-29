import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Validate
if not GOOGLE_MAPS_API_KEY:
    print("⚠️  WARNING: Google Maps API key not found")
    print("The app will work with mock data for testing")
    print("Add GOOGLE_MAPS_API_KEY to .env for real calculations")

if not GEMINI_API_KEY:
    print("ℹ️  INFO: Gemini API key not found")
    print("AI features will be disabled")
    print("Add GEMINI_API_KEY to .env for smart calculations")